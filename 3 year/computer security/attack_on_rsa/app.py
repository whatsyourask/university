import sys
# To import FastModularExponentiation
sys.path.insert(0, '..')
from additive_cipher.gui import *
from backend import AttackOnRSA
from time import time
import sys


class Application:
    """Logic of application"""
    def run(self) -> None:
        # Create all elements
        self._create_all_elements()
        # Start interface
        self._gui.start()

    def _create_all_elements(self) -> None:
        # Create all needed elements
        self._gui = GraphicUI()
        self._gui.set_title('Attack on RSA')
        width = 30
        self._gui.label('e', 1, 1, E)
        self._e_field, _ = self._gui.entry(StringVar(), 2, 1, width, W)
        self._gui.label('n', 1, 2, E)
        self._n_field, _ = self._gui.entry(StringVar(), 2, 2, width, W)
        self._gui.label('Encrypted text', 1, 3, W)
        self._encrypted_field = self._gui.text(2, 3, width, 5, W)
        self._gui.button('Attack', 3, 3, width, W, self._launch_attack)
        self._gui.label('p', 1, 4, E)
        self._p_field, _ = self._gui.entry(StringVar(), 2, 4, width, W)
        self._gui.label('q', 1, 5, E)
        self._q_field, _ = self._gui.entry(StringVar(), 2, 5, width, W)
        self._gui.label('d', 1, 6, E)
        self._d_field, _ = self._gui.entry(StringVar(), 2, 6, width, W)
        self._gui.label('Iterations count', 1, 7, E)
        self._iter_count_field, _ = self._gui.entry(StringVar(), 2, 7 , width, W)
        self._gui.label('Time', 1, 8, E)
        self._time_field, _ = self._gui.entry(StringVar(), 2, 8 , width, W)
        self._gui.label('Decrypted text', 1, 9, W)
        self._decrypted_field = self._gui.text(2, 9, width, 5, W)
        self._gui.button('Clear', 3, 9, width, W, self._clear)

    def _launch_attack(self):
        try:
            self._decrypted_field.delete("1.0", END)
            e = int(self._e_field.get())
            n = int(self._n_field.get())
            encrypted = self._encrypted_field.get("1.0", END)[:-1]
            time_start = time()
            print(sys.argv)
            print(len(sys.argv))
            if len(sys.argv) > 1 and sys.argv[1] == '1':
                aor = AttackOnRSA()
                attack = aor.threading_attack
                print('AttackOnRSA.threading_attack')
            else:
                attack = AttackOnRSA.attack
                print('AttackOnRSA.attack')
            p, q, d, decrypted, iter_count = attack(e, n, encrypted)
            time_end = time()
            time_diff = time_end - time_start
            self._p_field.set(p)
            self._q_field.set(q)
            self._d_field.set(d)
            self._iter_count_field.set(iter_count)
            self._time_field.set(time_diff)
            self._decrypted_field.insert(INSERT, decrypted)
        except ValueError:
            self._process_exception()

    def _process_exception(self) -> None:
        # Method to create a new window on top of main window
        self._gui.message_box('Ошибка', 'Неверные данные')

    def _clear(self):
        self._e_field.set('')
        self._n_field.set('')
        self._p_field.set('')
        self._q_field.set('')
        self._d_field.set('')
        self._iter_count_field.set('')
        self._time_field.set('')
        self._encrypted_field.delete("1.0", END)
        self._decrypted_field.delete("1.0", END)
