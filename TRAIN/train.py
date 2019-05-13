from __future__ import print_function
import random
import numpy as np
from collections import defaultdict, deque
from game import Board, Game
from mcts_pure import MCTSPlayer as MCTS_Pure #silly mcts tree
from mcts_alphaZero import MCTSPlayer #trained mcts tree
from tensorflow_net import PolicyValueNet


class TrainPipeline():
    def __init__(self, init_model=None):
        # params of the board and the game
        self.board_width = 15
        self.board_height = 15
        self.n_in_row = 5
        self.board = Board(width=self.board_width,
                           height=self.board_height,
                           n_in_row=self.n_in_row)
        self.game = Game(self.board)
        
        # training params
        self.batch_size = 512  # mini-batch size for training
        self.buffer_size = 10000
        self.data_buffer = deque(maxlen=self.buffer_size)
        self.c_puct = 5
        self.learn_rate = 0.002
        self.learn_rate_multiplier = 1.0  # adaptively adjust the learning rate based on KL
        self.n_playout = 400  # num of simulations for each move
        self.temp = 1.0  # the temperature param
        self.play_batch_size = 1
        self.epochs = 5  # num of train_steps for each update
        self.kl_targ = 0.02
        self.evaluate_step_num = 2
        self.game_batch_num = 1500
        self.best_win_ratio = 0
        self.pure_mcts_playout_num = 1000
        
        self.policy_value_net = PolicyValueNet(self.board_width,
                                               self.board_height,
                                               model_file=init_model)
        
        self.mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn,
                                      c_puct=self.c_puct,
                                      n_playout=self.n_playout,
                                      is_selfplay=1)

    def collect_selfplay_data(self, n_games=1):
        """collect self-play data for training"""
        for i in range(n_games):
            winner, play_data = self.game.start_self_play(self.mcts_player,
                                                          temp=self.temp)
            play_data = list(play_data)[:]
            self.episode_len = len(play_data)
            # augment the data
            extend_data = []
            for state, mcts_porb, winner in play_data:
                for i in [1, 2, 3, 4]:
                    # rotate counterclockwise
                    equi_state = np.array([np.rot90(s, i) for s in state])
                    equi_mcts_prob = np.rot90(np.flipud(
                        mcts_porb.reshape(self.board_height, self.board_width)), i)
                    extend_data.append((equi_state,
                                        np.flipud(equi_mcts_prob).flatten(),
                                        winner))
                    # flip horizontally
                    equi_state = np.array([np.fliplr(s) for s in equi_state])
                    equi_mcts_prob = np.fliplr(equi_mcts_prob)
                    extend_data.append((equi_state,
                                        np.flipud(equi_mcts_prob).flatten(),
                                        winner))
            
            self.data_buffer.extend(extend_data)

    def policy_update(self):
        """update the policy-value net"""
        mini_batch = random.sample(self.data_buffer, self.batch_size)
        state_batch = [data[0] for data in mini_batch]
        mcts_probs_batch = [data[1] for data in mini_batch]
        winner_batch = [data[2] for data in mini_batch]
        old_probs, old_v = self.policy_value_net.policy_value(state_batch)
        for i in range(self.epochs):
            loss, entropy = self.policy_value_net.train_step(
                    state_batch,
                    mcts_probs_batch,
                    winner_batch,
                    self.learn_rate*self.learn_rate_multiplier)
            new_probs, new_v = self.policy_value_net.policy_value(state_batch)
            kl = np.mean(np.sum(old_probs * (
                    np.log(old_probs + 1e-10) - np.log(new_probs + 1e-10)),
                    axis=1)
            )
            if kl > self.kl_targ * 4:  # early stopping if D_KL diverges badly
                break
        # adaptively adjust the learning rate
        if kl > self.kl_targ * 2 and self.learn_rate_multiplier > 0.1:
            self.learn_rate_multiplier /= 1.5
        elif kl < self.kl_targ / 2 and self.learn_rate_multiplier < 10:
            self.learn_rate_multiplier *= 1.5

        print("loss:{}".format(loss))
        return loss, entropy

    def policy_evaluate(self, n_games=10):
        """
        Evaluate the trained policy by playing against the pure MCTS player
        Note: this is only for monitoring the progress of training
        """
        current_mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn,
                                         c_puct=self.c_puct,
                                         n_playout=self.n_playout)
        pure_mcts_player = MCTS_Pure(c_puct=5,
                                     n_playout=self.pure_mcts_playout_num)
        win_cnt = defaultdict(int)
        for i in range(n_games):
            winner = self.game.start_play(current_mcts_player,
                                          pure_mcts_player,
                                          start_player=i % 2,
                                          is_shown=0)
            win_cnt[winner] += 1
        win_ratio = 1.0*(win_cnt[1] + 0.5*win_cnt[-1]) / n_games
        print("num_playouts:{}, win: {}, lose: {}, tie:{}".format(
                self.pure_mcts_playout_num,
                win_cnt[1], win_cnt[2], win_cnt[-1]))
        return win_ratio

    def run(self):
        for i in range(self.game_batch_num):
            self.collect_selfplay_data(self.play_batch_size)
            
            if len(self.data_buffer) > self.batch_size:
                loss, _ = self.policy_update()
                
            if (i+1) % self.evaluate_step_num == 0:
                print("Step: {0}".format(self.evaluate_step_num))
                win_ratio = self.policy_evaluate()
                self.policy_value_net.save_model('./current_policy.model')
                
                if win_ratio > self.best_win_ratio:
                    print("BEST POLICY REFRESHED!")
                    print("Win ratio: {0}".format(win_ratio))
                    self.best_win_ratio = win_ratio
                    # update the best_policy
                    self.policy_value_net.save_model('./best_policy.model')
                    
                    if (self.best_win_ratio == 1.0 and
                            self.pure_mcts_playout_num < 5000):
                        self.pure_mcts_playout_num += 1000
                        self.best_win_ratio = 0.0
        

if __name__ == '__main__':
    training_pipeline = TrainPipeline(init_model='./current_policy.model')
    training_pipeline.run()
