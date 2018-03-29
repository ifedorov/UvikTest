# Create your tests here.
from django.test import Client
from django.test import TestCase


class UvikTest(TestCase):
    def setUp(self):
        self.client = Client()

    def send(self, nplayers, board, deck, nsquares=None, ncards=None):
        return self.client.post('/', {'number_of_players': nplayers,
                                      'number_of_squares': nsquares or len(board),
                                      'number_of_cards': ncards or len(deck.split(',')),
                                      'board_sequence': board,
                                      'cards_in_deck': deck})

    def test_simple_ok(self):
        response = self.send(2, 'RYGPBRYGBRPOP', 'R, B, GG, Y, P, B, P, RR')
        assert 'instance' in response.context

    def test_input1_fail(self):
        response = self.send(4, 'RYGPBRYGBRPOP', 'R, B, GG, Y, P, B, P, RR')
        assert 'instance' in response.context
        self.assertEqual(response.context['instance'].result, "No player won after 8 cards.")

    def test_input1(self):
        '''
        Sample Input 1:
        Number of Players: 2
        Number of Squares on the board: 13
        Number of Cards in the deck: 8
        Sequence of characters on the board: RYGPBRYGBRPOP
        Cards in the deck: R, B, GG, Y, P, B, P, RR
        Sample Output 1:
        Player 1 won after 7 cards.
        '''

        response = self.send(2, 'RYGPBRYGBRPOP', 'R, B, GG, Y, P, B, P, RR', nsquares=13, ncards=8)
        self.assertEqual(response.context['instance'].result, 'Player 1 won after 7 cards.')

    def test_input2(self):
        '''
        Sample Input 2:
        Number of Players: 2
        Number of Squares on the board: 6
        Number of Cards in the deck: 5
        Sequence of characters on the board: RYGRYB
        Cards in the deck: R, YY, G, G, B
        Sample Output 2:

        Player 2 won after 4 cards.
        '''

        response = self.send(2, 'RYGRYB', 'R, YY, G, G, B', nsquares=6, ncards=5)
        self.assertEqual(response.context['instance'].result, 'Player 2 won after 4 cards.')

    def test_input3(self):
        '''
        Sample Input 3:
        Number of Players: 3
        Number of Squares on the board: 9
        Number of Cards in the deck: 6
        Sequence of characters on the board: QQQQQQQQQ
        Cards in the deck: Q, QQ, Q, Q, QQ, Q
        Sample Output 3:

        No player won after 6 cards.
        '''

        response = self.send(3, 'QQQQQQQQQ', 'Q, QQ, Q, Q, QQ, Q', nsquares=9, ncards=6)
        self.assertEqual(response.context['instance'].result, 'No player won after 6 cards.')

    def test_input4(self):
        '''
        Number of Players: 3
        Number of Squares on the board: 79
        Number of Cards in the deck: 10
        Sequence of characaters on the board:
        ABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLM
        NOPQRSTUVWXYABCD
        Cards in the deck: D, BB, CC, E, A, BB, EE, DD, CC, AA
        '''
        response = self.send(3, 'ABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCD',
                             'D, BB, CC, E, A, BB, EE, DD, CC, AA', nsquares=79, ncards=10)
        self.assertEqual(response.context['instance'].result, 'Player 2 won after 8 cards.')

    def test_input5(self):
        '''
        Number of Players: 1
        Number of Squares on the board: 10
        Number of Cards in the deck: 5
        Sequence of characters on the board: ABCDEABCDE
        Cards in the deck: A, B, A, BB, E
        '''
        response = self.send(1, 'ABCDEABCDE', 'A, B, A, BB, E', nsquares=10, ncards=5)
        self.assertEqual(response.context['instance'].result, 'Player 1 won after 4 cards.')

    def test_input6(self):
        '''
        Number of Players: 1
        Number of Squares on the board: 10
        Number of Cards in the deck: 5
        Sequence of characters on the board: ABCDEABCDE
        Cards in the deck: A, B, A, BB, E
        '''
        response = self.send(4, 'Z', 'X', nsquares=1, ncards=1)
        self.assertEqual(response.context['instance'].result, 'Player 1 won after 1 cards.')

    def test_input7(self):
        '''
        Number of Players: 4
        Number of Squares: 79
        Number of Cards in the deck: 200
        Sequence of characters on the board:
        ABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLM
        NOPQRSTUVWXYABCD
        Cards in the deck: A, A, A, A, B, B, B, B, C, C, C, C, D, D, D, D, E, E, E, E, F, F, F, F, G, G, G,
        G, H, H, H, H, I, I, I, I, J, J, J, J, K, K, K, K, L, L, L, L, M, M, M, M, N, N, N, N, O, O, O, O, P, P,
        P, P, Q, Q, Q, Q, R, R, R ,R, S, S, S, S, T, T, T, T, U, U, U, U, V, V, V, V, W, W, W, W, X, X, X,
        X, Y, Y, Y, Y, A, A, A, A, B, B, B, B, C, C, C, C, D, D, D, D, E, E, E, E, F, F, F, F, G, G, G, G, H,
        H, H, H, I, I, I, I, J, J, J, J, K, K, K, K, L, L, L, L, M, M, M, M, N, N, N, N, O, O, O, O, P, P, P, P,
        Q, Q, Q, Q, R, R, R, R, S, S, S, S, T, T, T, T, U, U, U, U, V, V, V, V, W, W, W, W, X, X, X, X, Y,
        Y, Y, Y
        '''
        response = self.send(4, 'ABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCD',
                             '''
                             A, A, A, A, B, B, B, B, C, C, C, C, D, D, D, D, E, E, E, E, F, F, F, F, G, G, G,
                             G, H, H, H, H, I, I, I, I, J, J, J, J, K, K, K, K, L, L, L, L, M, M, M, M, N, N, N, N, O, O, O, O, P, P,
                             P, P, Q, Q, Q, Q, R, R, R ,R, S, S, S, S, T, T, T, T, U, U, U, U, V, V, V, V, W, W, W, W, X, X, X,
                             X, Y, Y, Y, Y, A, A, A, A, B, B, B, B, C, C, C, C, D, D, D, D, E, E, E, E, F, F, F, F, G, G, G, G, H,
                             H, H, H, I, I, I, I, J, J, J, J, K, K, K, K, L, L, L, L, M, M, M, M, N, N, N, N, O, O, O, O, P, P, P, P,
                             Q, Q, Q, Q, R, R, R, R, S, S, S, S, T, T, T, T, U, U, U, U, V, V, V, V, W, W, W, W, X, X, X, X, Y,
                             Y, Y, Y
                             ''', nsquares=79, ncards=200)
        errors = {key: value for key, value in response.context['form'].errors.items()}
        self.assertEqual(response.context['instance'].result, 'No player won after 200 cards.')

    def test_input8(self):
        '''
        Number of Players: 4

        Number of Squares: 79
        Number of Cards in the deck: 100
        Sequence of characters on the board:
        ABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLM
        NOPQRSTUVWXYABCD
        Cards in the deck: A, A, A, A, B, B, B, B, C, C, C, C, D, D, D, D, E, E, E, E, F, F, F, F, G, G, G,
        G, H, H, H, H, I, I, I, I, J, J, J, J, K, K, K, K, L, L, L, L, M, M, M, M, N, N, N, N, O, O, O, O, P, P,
        P, P, Q, Q, Q, Q, R, R, R, R, S, S, S, S, T, T, T, T, U, U, U, U, V, V, V, V, W, W, W, W, X, X, X,
        X, Y, Y, Y, Z
        '''
        response = self.send(4, 'ABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCDEFGHIJKLMNOPQRSTUVWXYABCD',
                             '''A, A, A, A, B, B, B, B, C, C, C, C, D, D, D, D, E, E, E, E, F, F, F, F, G, G, G,
        G, H, H, H, H, I, I, I, I, J, J, J, J, K, K, K, K, L, L, L, L, M, M, M, M, N, N, N, N, O, O, O, O, P, P,
        P, P, Q, Q, Q, Q, R, R, R, R, S, S, S, S, T, T, T, T, U, U, U, U, V, V, V, V, W, W, W, W, X, X, X,
        X, Y, Y, Y, Z
        ''', nsquares=79, ncards=100)
        self.assertEqual(response.context['instance'].result, 'Player 4 won after 100 cards.')

    def test_100_players(self):
        response = self.send(100, 'QQQQQQQQQ', 'Q, QQ, Q, Q, QQ, Q', nsquares=9, ncards=6)
        errors = {key: value for key, value in response.context['form'].errors.items()}
        self.assertEqual(errors['number_of_players'][0], 'Ensure this value is less than or equal to 4.')
