import torch
import random 
from Models import PigModel

class MnistTrainer:
    def __init__(self, model, optimizer, loss_fn, train_loader, device='cuda'):

        self.model = model.to(device)
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.train_loader = train_loader
        self.device = device

    def trainEpoch(self):
        # Set all players' models to training mode.
        for player in self.players:
            player.model.train() 
            
        total_loss = [0.0 for _ in range(len(self.players))]
        
        # Iterate over each player's stored SAR data.
        for idx, player in enumerate(self.players):
            for batch in self.sar[idx]:
                # Unpack the stored tuple.
                # Here, 'state' is a list/tuple of features,
                # 'action' is 1 if the player chose to roll, 0 if they passed,
                # 'reward' is the reward, and we ignore any stored probability.
                state, action, reward, _ = batch
                
                # Recompute the probability from the state.
                input_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(self.device)
                output = player.model(input_tensor)
                # Assume that output[0, 0] is the probability of rolling.
                roll_probability = output[0, 0]
                
                # Determine the probability corresponding to the taken action.
                # If action==1 (roll), use roll_probability.
                # Otherwise (action==0, pass), use 1 - roll_probability.
                if action == 1:
                    prob = roll_probability
                else:
                    prob = 1 - roll_probability
                    
                # Compute the loss for this sample.
                # For policy gradients, you might use:
                #   loss = -log(prob) * reward
                loss = -torch.log(prob) * reward
                
                # Backpropagate the loss.
                self.optimizers[idx].zero_grad()
                loss.backward()
                self.optimizers[idx].step()
                
                total_loss[idx] += loss.item()
        
        # Compute the average loss per player.
        average_loss = []
        for idx, loss in enumerate(total_loss):
            num_batches = len(self.sar[idx])
            average_loss.append(loss / num_batches if num_batches > 0 else 0)
            
        return average_loss

    def train(self, num_epochs, print_every=1):
        """
        Runs the training loop for a given number of epochs.
        
        Args:
            num_epochs (int): Number of epochs to train.
            print_every (int): Frequency (in epochs) to print the loss.
        """
        for epoch in range(num_epochs):
            epoch_loss = self.train_epoch()
            if (epoch + 1) % print_every == 0:
                print(f"Epoch {epoch+1}/{num_epochs} - Loss: {epoch_loss:.4f}")
                
    def save_model(self, file_path):
        """
        Saves the trained model's state dictionary to a file.
        
        Args:
            file_path (str): The path where the model state will be saved.
        """
        torch.save(self.model.state_dict(), file_path)

class PigTrainer:

    def __init__(self, player_amount,  device='cpu'):
        self.device = device
        self.WINNING_SCORE = 100
        self.print_game = False
        self.sar = [[] for _ in range(player_amount)]
        self.players = []
        for i in range(player_amount):
            self.players.append(AIBotPlayer("aibot " + str(i), PigModel(), True))
        
        self.optimizers = [torch.optim.Adam(player.model.parameters(), lr=0.001) for player in self.players]
        self.lowestLoss = 1
        self.lowestLossPlayer = AIBotPlayer("lowestBot", PigModel(), True)

    def getPlayer0(self):
        return self.players[0]

    # def trainEpoch(self):
    #     for player in self.players:
    #         player.model.train() 
            
    #     total_loss = [0.0 for _ in range(len(self.players))]
    #     for idx, player in enumerate(self.players):
    #         for batch in self.sar[idx]:
    #             # Unpack the batch correctly
    #             inputs, action, reward, probobility = batch
    #             lossTuples = [(probobility, reward)]
    #             self.optimizers[idx].zero_grad()
    #             loss = self.logLoss(lossTuples)
    #             loss.backward()
    #             self.optimizers[idx].step()
    #             total_loss[idx] += loss.item()
        
    #     average_loss = []
    #     for idx, loss in enumerate(total_loss):
    #         num_batches = len(self.sar[idx])
    #         average_loss.append(loss / num_batches if num_batches > 0 else 0)

            
    #     return average_loss
    
    def trainEpoch(self):
        # Set all players' models to training mode.
        for player in self.players:
            player.model.train() 
            
        total_loss = [0.0 for _ in range(len(self.players))]
        
        # Iterate over each player's stored SAR data.
        for idx, player in enumerate(self.players):
            for batch in self.sar[idx]:
                # Unpack the stored tuple.
                # 'state' is a list/tuple of features,
                # 'action' is 1 if the player chose to roll, 0 if they passed,
                # 'reward' is the reward.
                state, action, reward, _ = batch

                # Recompute the probability from the stored state.
                input_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(self.device)
                output = player.model(input_tensor)
                # Assume that output[0, 0] is the probability of rolling.
                roll_probability = output[0, 0]
                
                # Determine the probability corresponding to the taken action.
                # If action == 1 (roll), use roll_probability.
                # Otherwise (action == 0, pass), use 1 - roll_probability.
                prob = roll_probability if action == 1 else (1 - roll_probability)
                
                # Ensure reward is a tensor on the correct device.
                reward_tensor = torch.tensor(reward, dtype=torch.float32, device=self.device)
                
                # Compute the loss for this sample.
                # For policy gradients, a common loss is:
                #    loss = -log(prob) * reward
                prob = torch.clamp(prob, min=1e-6, max=1 - 1e-6)

                loss = -torch.log(prob) * reward_tensor
                
                if loss > 0 and loss < self.lowestLoss:
                    self.lowestLoss = loss
                    self.lowestLossPlayer.model.load_state_dict(player.model.state_dict())
                    
                
                # Backpropagate the loss.
                self.optimizers[idx].zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(player.model.parameters(), max_norm=1.0)
                self.optimizers[idx].step()
                
                total_loss[idx] += loss.item()
        
        # Compute the average loss per player.
        average_loss = []
        for idx, loss_val in enumerate(total_loss):
            num_batches = len(self.sar[idx])
            average_loss.append(loss_val / num_batches if num_batches > 0 else 0)
            
        return average_loss

    def save_model(self, file_path):
        """
        Saves the trained model's state dictionary to a file.
        
        Args:
            file_path (str): The path where the model state will be saved.
        """
        whowon = [0] * len(self.players)
        for _ in range(1000):
            piggy = PassThePigs(len(self.players), self.print_game)
            player_number, won = self.reset(piggy, len(self.players))
            
            while not won:
                self.one_player_turn(player_number, self.players, piggy)
                self.display_game_status(self.players, piggy)

                if piggy.get_player_bank(player_number) >= self.WINNING_SCORE:
                    won = True
                    if self.print_game:
                        print("Game over! Winner is: " + self.players[player_number].get_name())
                else:
                    player_number = (player_number + 1) % len(self.players)
        max_value = max(whowon)
        max_index = whowon.index(max_value)
        torch.save(self.lowestLossPlayer.model.state_dict(),"./models/lowestloss.pth")
        torch.save(self.players[max_index].model.state_dict(), file_path)
    
    def train(self) :
        piggy = PassThePigs(len(self.players), self.print_game)
        player_number, won = self.reset(piggy, len(self.players))
        
        while not won:
            self.one_player_turn(player_number, self.players, piggy)
            self.display_game_status(self.players, piggy)

            if piggy.get_player_bank(player_number) >= self.WINNING_SCORE:
                won = True
                # At the end of game:
                for state, action, reward, prob in self.sar[player_number]:
                    reward += .5  # Big boost for winning game

                if self.print_game:
                    print("Game over! Winner is: " + self.players[player_number].get_name())
            else:
                player_number = (player_number + 1) % len(self.players)
        
        
        print("epoch done")        
        print(self.trainEpoch())
        self.sar = [[] for _ in range(len(self.players))]
        
    def one_player_turn(self, player_number, players, piggy):
        pigged_out = False
        passed = False
        
        while not pigged_out and not passed:
            state = [piggy.get_player_bank(player_number),
            piggy.get_hand_value(),
            players[player_number].most_dangerous_opponent_proximity(piggy.get_players_bank_values(player_number), self.WINNING_SCORE),
            self.WINNING_SCORE]
            
            player_wants_to_role, probobility =  players[player_number].wants_to_roll(
                piggy.get_player_bank(player_number),
                piggy.get_hand_value(),
                piggy.get_players_bank_values(player_number),
                self.WINNING_SCORE
            )
            if player_wants_to_role:
                if self.print_game:
                    print(f"{players[player_number].get_name()} rolls a ", end="")
                pigged_out, hand_value = piggy.player_role_pigs()
                self.sar[player_number].append((state, 1, (hand_value - state[1]) * 0.003, probobility))
            else:
                if self.print_game:
                    print(f"{players[player_number].get_name()} passes")
                passed = True
                self.sar[player_number].append((state, 0, state[1] * 0.008 , probobility))
        piggy.change_player_bank_after_round(player_number)

    def display_game_status(self, players, piggy):
        if self.print_game:
            for i, player in enumerate(players):
                print(f"{player.get_name()}: {piggy.get_player_bank(i)} | ", end="")
            print()
            
    def reset(self, piggy, amount_of_players):
        piggy.reset()
        player_number = random.randint(0, amount_of_players - 1)
        won = False
        return player_number, won

    