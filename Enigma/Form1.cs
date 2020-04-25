using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Enigma
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            
            // По умолчанию выбранные элементы
            int startBoxItem = 0;
            comboBox1.SelectedIndex = startBoxItem;
            comboBox2.SelectedIndex = startBoxItem;
            comboBox3.SelectedIndex = startBoxItem;
            comboBox4.SelectedIndex = startBoxItem;
            comboBox5.SelectedIndex = startBoxItem;
            comboBox6.SelectedIndex = startBoxItem;
            comboBox7.SelectedIndex = startBoxItem;
            comboBox9.SelectedIndex = startBoxItem;
            comboBox10.SelectedIndex = startBoxItem;
            comboBox11.SelectedIndex = startBoxItem;
        }

        // Исходный текст
        string inputText;

        // Обработанный текст
        string outputText;

        // Коммутирующие буквы
        string plugString;

        // Коммутация букв
        Dictionary<char, char> plugLetters;

        // 3 ротора машины
        Rotor rot1;
        Rotor rot2;
        Rotor rot3;

        // Рефлектор
        Reflector reflect;

        // Функция для вставки пробелов в выходную строку
        private void FormatOutput()
        {
            // Вставить пробелы в строку через каждые 5 символов
            char space = ' ';

            // Длина 1 закодированной последовательности
            int wordLength = 5;

            // Количество итераций
            int iterCount = outputText.Length / wordLength;
            for (int i = 0; i < iterCount; i++)
            {
                // Индекс, по которому вставляется пробел
                int addIndex = (i + 1) * wordLength;
                outputText = outputText.Insert(addIndex + i, space.ToString());
            }

            // Сделать нижний регистр
            outputText = outputText.ToLower();
        }

        // Функция шифрования 1 буквы
        // Принимает на вход букву для преобразований
        private char EncodeDecodeLetter(char letter)
        {
            // Объявить результирующую букву
            char resultLetter;

            // Посмотреть не соединена ли буква на plugboard
            if (plugString != "")
                resultLetter = LetterSwitch(letter);

            // Инициализировать переменную для прохождения
            // вперёд по роторам до рефлектора 1-ей
            int toward = 1;

            // Инициализировать переменную для прохождения
            // назад по роторам от рефлектора -1-ей
            int back = -1;

            // Вызвать функцию ротора проход вперёд для всех 3 роторов
            resultLetter = rot1.PassThrough(letter, toward);
            resultLetter = rot2.PassThrough(resultLetter, toward, rot1.GetLetter());
            resultLetter = rot3.PassThrough(resultLetter, toward, rot2.GetLetter());
            resultLetter = rot3.GetDiffLetter(resultLetter);

            // Вызвать функцию рефлектора с проходом по нему
            resultLetter = reflect.PassThrough(resultLetter);

            // Вызвать функцию ротора проход назад для всех 3 роторов
            resultLetter = rot3.PassThrough(resultLetter, back);
            resultLetter = rot2.PassThrough(resultLetter, back, rot3.GetLetter());
            resultLetter = rot1.PassThrough(resultLetter, back, rot2.GetLetter());
            resultLetter = rot1.GetDiffLetter(resultLetter);

            // Посмотреть не соединена ли буква на plugboard
            if (plugString != "")
                resultLetter = LetterSwitch(letter);

            // Вернуть результат
            return resultLetter;
        }

        // Функция для коммутации буквы
        private char LetterSwitch(char letter)
        {
            // В глобальном словаре найти коммутирующую букву
            // если нет - ок, если да - заменить ею и передать в функцию шифрования
            return plugLetters.ContainsKey(letter) ? plugLetters[letter] : letter;
        }

        // Функция шифрования
        private void EncodeDecodeText() 
        {
            // Инициализировать временную переменную для хранения результата
            string encodeString = "";

            // цикл по длине строки
            for (int i = 0; i < inputText.Length; i++)
            {
                // Переменная для выбранной буквы, которая может быть изменена на коммутирующую
                // Чтобы не менять исходный текст
                char chosenLetter = inputText[i];

                // Если проход через 1 ротор, повернуть его на 1 вперёд при обратном проходе
                rot1.LetterShift(comboBox5);

                // Если ротор 1 при повороте проходит позицию буквы,
                // при которой поворачивается 2 ротор, то он поворачивает 2 ротор
                if (rot1.GetLetter() == rot1.GetTurnChar())
                    rot2.LetterShift(comboBox6);

                // Если ротор 2 при повороте проходит позицию буквы,
                // при которой поворачивается 3 ротор, то он поворачивает 3 ротор
                if (rot2.GetLetter() == rot2.GetTurnChar())
                    rot3.LetterShift(comboBox7);

                // Преобразовать букву
                chosenLetter = EncodeDecodeLetter(chosenLetter);

                // Прибавить к результату
                encodeString += chosenLetter;
            }

            // Присвоить переменной обработанного текста
            outputText = encodeString;
        }

        // Функция для поиска коммутирующих букв
        // На входе строка из рефлектора
        private void GetPlugboard()
        {
            // Разбить строку на подстроки используя пробелы между парами
            string[] plugLettersArr = plugString.Split(' ');

            // В цикле в итой подстроке взять 0 и 1 элементы и засунуть их в глобальные словари
            plugLetters = new Dictionary<char, char>(plugLettersArr.Length * 2);
            foreach (string elem in plugLettersArr)
            {
                plugLetters.Add(elem[0], elem[1]);
                plugLetters.Add(elem[1], elem[0]);
            }
        }

        // Функция для форматирования текста
        private void FormatInput()
        {
            // Индекс первого пробела
            int space = inputText.IndexOf(' ');

            // Удалить в цикле пробелы
            while (space != -1) {
                inputText = inputText.Remove(space, 1);
                space = inputText.IndexOf(' ');
            }

            // сделать верхний регистр
            inputText = inputText.ToUpper();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Rotor.UpdateCountOfRotors();

            // Взять исходный текст
            inputText = richTextBox1.Text;

            // Запустить функцию для форматирования исходного текста
            FormatInput();

            // Инициализировать объекты роторов и поставить параметры из comboBox
            rot1 = new Rotor();
            int rotNum1 = Convert.ToInt32(comboBox1.SelectedItem);
            char chosenLetter1 = Convert.ToChar(comboBox5.SelectedItem);
            char chosenRing1 = Convert.ToChar(comboBox9.SelectedItem);
            rot1.SetRotor(rotNum1, chosenLetter1, chosenRing1);

            rot2 = new Rotor();
            int rotNum2 = Convert.ToInt32(comboBox2.SelectedItem);
            char chosenLetter2 = Convert.ToChar(comboBox6.SelectedItem);
            char chosenRing2 = Convert.ToChar(comboBox10.SelectedItem);
            rot2.SetRotor(rotNum2, chosenLetter2, chosenRing2);

            rot3 = new Rotor();
            int rotNum3 = Convert.ToInt32(comboBox3.SelectedItem);
            char chosenLetter3 = Convert.ToChar(comboBox7.SelectedItem);
            char chosenRing3 = Convert.ToChar(comboBox11.SelectedItem);
            rot3.SetRotor(rotNum3, chosenLetter3, chosenRing3);

            // Взять из plugboard строку и найти, коммутирующие буквы
            plugString = textBox1.Text.ToUpper();
            if (plugString != "")
                GetPlugboard();

            // Инициализировать объект рефлектор и настроить
            reflect = new Reflector();
            char chosenReflector = Convert.ToChar(comboBox4.SelectedItem);
            reflect.SetReflector(chosenReflector);

            // Запустить функцию шифрования
            EncodeDecodeText();

            // Запустить функцию для форматирования выходного текста и передать в richTextBox
            FormatOutput();
            richTextBox2.Text = outputText;
        }
    }

    // Класс ротора
    class Rotor
    {
        // Словарь, где ключ - номер ротера, а значение - кодировка букв
        static Dictionary<int, string> rotorPresets = new Dictionary<int, string>(3)
        {
            { 1, "EKMFLGDQVZNTOWYHXUSPAIBRCJ"},
            { 2, "AJDKSIRUXBLHWTMCQGZNPYFVOE"},
            { 3, "BDFHJLCPRTXVZNYEIWGAKMUSQO"}
        };

        // Словарь с буквами, на которые роторы должны повернуться
        static Dictionary<int, char> rotorTurns = new Dictionary<int, char>(2)
        {
            {1, 'R' },
            {2, 'F' },
        };
 
        // Английский алфавит
        const string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

        // Длина алфавита, чтобы не вычислять Length
        const int alphLength = 26;

        // Кодировка букв у ротора с номером number
        string currentPreset;

        // Начальную буква, что выбирается на роторе
        char currentLetter;

        // Счётчик кол-ва созданных объектов
        static int countOfRotors;

        // Порядковый номер ротора
        int accountRotor;

        // Конструктор, в котором считается кол-во созданных экземпляров и назначается им номер
        public Rotor()
        {
            countOfRotors++;
            accountRotor = countOfRotors;
        }

        // Настроить ротор
        public void SetRotor(int chosenNumber, char letter, char ring)
        {   
            // Сделать его кодировку нижним регистром
            currentPreset = rotorPresets[chosenNumber];

            // Назначить букву, поставленную в роторе
            currentLetter = letter;

            // Поставить начальную позицию кольца
            SetRingPosition(ring);
        }

        // Геттер буквы ротора
        public char GetLetter()
        {
            return currentLetter;
        }

        // Метод сдвига буквы в роторе на 1
        public void LetterShift(ComboBox box)
        {
            // Индекс буквы в алфавите
            int alphInd = alphabet.IndexOf(currentLetter);

            // Деление по модулю длины словаря
            currentLetter = alphabet[(alphInd + 1) % alphLength];

            // Обновление комбобокса
            UpdateComboBox(box);
        }

        // Обновить содержимое бокса
        public void UpdateComboBox(ComboBox box)
        {
            box.SelectedItem = box.Items[(box.SelectedIndex + 1) % alphLength];
        }

        // Метод для постановки начальной позиции ring
        void SetRingPosition(char ring)
        {   
            // Взять строку пресета и разрезать пополам
            int divideInd = currentPreset.IndexOf(ring);
            string firstSubStringPreset = currentPreset.Substring(0, divideInd);
            int endInd = currentPreset.Length - divideInd;
            string secondSubStringPreset = currentPreset.Substring(divideInd, endInd);

            // Склеить эти 2 строки, поменяв местами
            currentPreset = secondSubStringPreset + firstSubStringPreset;
        }

        // Метод прохода через ротор
        // Получает букву на вход(Только её, если 1 ротор вызывает)
        // Если остальные, то ещё режим(если 1, то вперёд, если -1, то назад) и букву предыдущего ротора
        public char PassThrough(char letter, int mode, char prevRotorLetter = ' ')
        {
            // Индекс буквы в таблице ротора, после преобразований
            int needIndex;

            // Индекс буквы в роторе
            int rotLetterInd = alphabet.IndexOf(currentLetter);
            
            // Индекс буквы на входе
            int inputLetterInd = alphabet.IndexOf(letter);

            // Если вызывает 1-ый ротор и проход вперёд по роторам или 3-ий ротор, но проход назад, то
            if ((accountRotor == 1 && mode == 1) || (accountRotor == 3 && mode == -1))
            {
                // Прибавить к индексу буквы в роторе индекс буквы, полученной на входе, по модулю 26
                needIndex = (rotLetterInd + inputLetterInd) % alphLength;
            }
            else
            {
                // Вычислить разницу между буквами текущего и предыдущего роторов
                // Прибавить разницу к индексу буквы, полученной на входе
                // или вычесть из него в зависимости от режима
                // Режим: если 1, значит вперёд к рефлектору, если -1, значит от рефлектора на выход

                // Индекс буквы на предыдущем роторе
                int prevRotLetterInd = alphabet.IndexOf(prevRotorLetter); 

                // Разница между буквами роторов, умноженная на режим
                // Если от рефлектора, то буквы роторов вычитаются поменявшись местами, необходимо обратное,
                // поэтому умножается на режим, т.е. на -1
                int betweenCurAndPrev = (rotLetterInd - prevRotLetterInd) * mode;

                // Если разница отрицательна, значит необходимо взять индекс с конца
                if (betweenCurAndPrev < 0)
                    betweenCurAndPrev = alphLength - Math.Abs(betweenCurAndPrev);

                // Если вперёд к рефлектору, то просто суммировать с индексом буквы
                if (mode == 1)
                    needIndex = Math.Abs(inputLetterInd + betweenCurAndPrev) % alphLength;
                else
                {
                    // Разница между входной буквой и разницой букв роторов
                    int betweenInputAndDiff = inputLetterInd - betweenCurAndPrev;

                    // Если разница отрицательная, взять индекс с конца
                    if (betweenInputAndDiff < 0)
                        betweenInputAndDiff = alphLength - Math.Abs(betweenInputAndDiff);
                    needIndex = betweenInputAndDiff % alphLength;
                }
            }

            // Вернуть букву, что становится равной букве из таблицы ротора, исходя из индекса, если проход вперёд по роторам
            // Иначе же взять букву, что преобразуется обратно из таблицы ротора, исходя из индекса буквы в таблице ротора
            if (mode == 1)
                return currentPreset[needIndex];
            else
            {
                // Найти символ с нужным индексом сначала в алфавите
                char inAlphInd = alphabet[needIndex];

                // Потом найти индекс символа в таблице ротора и узнать его индекс
                int inPresetInd = currentPreset.IndexOf(inAlphInd);

                // Взять из алфавита букву, соответствующую этому индексу
                return alphabet[inPresetInd];
            } 
        }

        // Метод для вычисления разности двух букв
        public char GetDiffLetter(char letter)
        {
            // Вычесть из текущей буквы букву на роторе
            int betweenInputAndCur = alphabet.IndexOf(letter) - alphabet.IndexOf(currentLetter);

            // Если разница отрицательная, взять индекс с конца
            if (betweenInputAndCur < 0)
                betweenInputAndCur = alphLength - Math.Abs(betweenInputAndCur);
            int ind = betweenInputAndCur;

            // Найти в алфавите по индексу букву и возвращаем
            return alphabet[ind];
        }
        
        // Геттер буквы поворота ротора
        public char GetTurnChar()
        {
            return rotorTurns[accountRotor];
        }

        // Обнуляет кол-во экземпляров класса
        public static void UpdateCountOfRotors()
        {
            countOfRotors = 0;
        }

        // Для теста алгоритма на 1 роторе для 1 буквы
        public void TestRot1()
        {
            int rotNum1 = 1;
            char chosenLetter1 = 'Q';
            char chosenRing1 = 'E';
            SetRotor(rotNum1, chosenLetter1, chosenRing1);
        }

        // Аналогично для 2 ротора
        public void TestRot2()
        {
            int rotNum2 = 2;
            char chosenLetter2 = 'U';
            char chosenRing2 = 'A';
            SetRotor(rotNum2, chosenLetter2, chosenRing2);
        }

        // Аналогично для 3 ротора
        public void TestRot3()
        {
            int rotNum3 = 3;
            char chosenLetter3 = 'C';
            char chosenRing3 = 'B';
            SetRotor(rotNum3, chosenLetter3, chosenRing3);
        }
    }

    // Класс рефлектора
    class Reflector
    {
        // Словарь, где ключ - выбранный рефлектор, а значение соответствующий словарь отражений
        static Dictionary<char, Dictionary<char, char>> reflectPresets = new Dictionary<char, Dictionary<char, char>>(2)
        {
            {'B', new Dictionary<char, char>(13)
                {   {'A', 'Y'},
                    {'B', 'R'},
                    {'C', 'U'},
                    {'D', 'H'},
                    {'E', 'Q'},
                    {'F', 'S'},
                    {'G', 'L'},
                    {'H', 'D'},
                    {'I', 'P'},
                    {'J', 'X'},
                    {'K', 'N'},
                    {'L', 'G'},
                    {'M', 'O'},
                    {'N', 'K'},
                    {'O', 'M'},
                    {'P', 'I'},
                    {'Q', 'E'},
                    {'R', 'B'},
                    {'S', 'F'},
                    {'T', 'Z'},
                    {'U', 'C'},
                    {'V', 'W'},
                    {'W', 'V'},
                    {'X', 'J'},
                    {'Y', 'A'},
                    {'Z', 'T'}
                }
            },
            {'C', new Dictionary<char, char>(13)
                {   {'A', 'F'},
                    {'B', 'V'},
                    {'C', 'P'},
                    {'D', 'J'},
                    {'E', 'I'},
                    {'F', 'A'},
                    {'G', 'O'},
                    {'H', 'Y'},
                    {'I', 'E'},
                    {'J', 'D'},
                    {'K', 'R'},
                    {'L', 'Z'},
                    {'M', 'X'},
                    {'N', 'W'},
                    {'O', 'G'},
                    {'P', 'C'},
                    {'Q', 'T'},
                    {'R', 'K'},
                    {'S', 'U'},
                    {'T', 'Q'},
                    {'U', 'S'},
                    {'V', 'B'},
                    {'W', 'N'},
                    {'X', 'M'},
                    {'Y', 'H'},
                    {'Z', 'L'}
                }
            }
        };

        // Словарь для текущего выбранного рефлектора
        Dictionary<char, char> currentPreset;

        // Настроить рефлектор
        public void SetReflector(char chosenReflector)
        {
            currentPreset = reflectPresets[chosenReflector];
        }
        
        // Метод прохода через рефлектор
        public char PassThrough(char letter)
        {
            // Возвращаем букву соответствующую букве на входе в таблице рефлектора
            return currentPreset[letter];
        }
    }
}