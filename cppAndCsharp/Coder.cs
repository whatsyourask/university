using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace lesson7
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        string bufferOrigText = ""; // Буфер для исходного текста
        string bufferCipheredText; // Буфер для шифрованного текста
        int n; // смещение для шифра Цезаря
        string keyword = ""; // Буфер для введённого ключевого слова
        int[] N_1;
        int[] N_2;
        string bufferDecipheredText;
        // Кнопка запуска шифра Цезаря
        private void button1_Click(object sender, EventArgs e)
        {
            bufferCipheredText = ""; // Обнуляем richTextBox2 
            string alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"; // Вспомогательный буфер для выполнения шифра
            bufferOrigText = richTextBox1.Text; // Заносим в bufferOrigText исходный текст из richTextBox1
            bool ciph; // Булевая переменная для выхода из цикла
            n = Convert.ToInt32(textBox1.Text); // Конвертируем сдвиг,получаемый из textBox1 в int
            // Берём по 1 букве исходного текста,сравниваем с буквами вспомогательного буфера
            // Если нашли одинаковую,сдвигаем на (j+n) % caesar.Length
            // Вычисляем остаток,чтобы не уйти за границы вспомогательго массива
            for (int i = 0; i < bufferOrigText.Length; i++)
            {
                ciph = true;
                for(int j = 0; j < alphabet.Length && ciph == true; j++)
                {
                    if (bufferOrigText[i] == alphabet[j])
                    {
                        bufferCipheredText += alphabet[(j + n) % alphabet.Length]; 
                        ciph = false;
                    }
                }
            }
            richTextBox2.Text = bufferCipheredText; // Заносим в richTextBox2 зашифрованный текст
        }
        // Кнопка запуска шифра Виженера
        private void button2_Click(object sender, EventArgs e)
        {
            bufferCipheredText = ""; // Обнуляем richTextBox2 
            bufferOrigText = richTextBox1.Text; // Заносим в bufferOrigText исходный текст из richTextBox1
            string alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"; // Вспомогательный буфер для выполнения шифра
            keyword = textBox2.Text; // Заносим в кодовое слово textBox2.Text
            string repeatWord = ""; // Буфер для записи кодового слова циклически до тех пор,пока не заполнится вся длина исходного текста
            keyword.ToLower();
            bufferOrigText.ToLower();
            // Записываем сначала слово полностью,что вместятся
            for(int i=0;i<bufferOrigText.Length / keyword.Length; i++)
            {
                repeatWord += keyword;
            }
            // Если можно записать ещё часть слова,то пишем и её по букве
            if (bufferOrigText.Length % keyword.Length != 0)
                for (int i = 0; i < keyword.Length; i++)
                {
                    repeatWord += keyword[i];
                }
            bool ciph; // Булевая переменная для выхода из цикла
            for (int i = 0; i < bufferOrigText.Length; i++)
            {
                ciph = true;
                for (int j = 0; j < alphabet.Length && ciph == true; j++)
                {
                    if (repeatWord[i] == alphabet[j])
                    {
                        int x = Math.Abs(repeatWord[i] - bufferOrigText[i]);
                        bufferCipheredText += alphabet[(j + x) % alphabet.Length];
                        ciph = false;
                    }
                }
            }
            richTextBox2.Text = bufferCipheredText; // Заносим в richTextBox2 зашифрованный текст
        }
        // Выбираем файл
        private void button9_Click(object sender, EventArgs e)
        {
            openFileDialog1.Filter = "txt files(*.txt|*.txt|All files (*.*)|*.*)";
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                // Копируем имя
                string fileName = openFileDialog1.FileName;
                // Создаём объект класса Filestream(для управления потоком)
                FileStream filestream = File.Open(fileName, FileMode.Open, FileAccess.Read);
                // Если что-то есть в потоке,то выполняем блок
                if (filestream != null)
                {
                    // Создаём объект класса StreamReader для чтения из потока 
                    StreamReader streamreader = new StreamReader(filestream);
                    // Считываем в richTextBox1
                    richTextBox1.Text = streamreader.ReadToEnd();
                    // Закрываем поток
                    filestream.Close();
                }
            }
        }
        // Строим график исходного текста
        private void button7_Click(object sender, EventArgs e)
        {
            // Очищаем chart1
            chart1.Series[0].Points.Clear();
            string[] alphabet = { "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я" }; // Вспомогательный буфер
            bufferOrigText = richTextBox1.Text; // Вставляем текст
            N_1 = new int[alphabet.Length]; // Массив для подсчёта частоты букв
            for (int i = 0; i < alphabet.Length; i++)
            {
                N_1[i] = 0;
                for (int j = 0; j < bufferOrigText.Length; j++)
                {
                    if (alphabet[i] == Convert.ToString(bufferOrigText[j]))
                        N_1[i]++;
                }
                // Выводим в richTextBox3
                richTextBox3.Text += " " + alphabet[i] + " " + N_1[i] + "\n";
            }
            for (int i = 0; i < alphabet.Length; i++)
            {
                for (int k = i + 1; k < alphabet.Length; k++)
                {
                    if (N_1[i] < N_1[k])
                    {
                        int temp = N_1[i];
                        N_1[i] = N_1[k];
                        N_1[k] = temp;

                        string temps = alphabet[i];//меняем буквы в алфавите в соответствии с их кол-вом
                        alphabet[i] = alphabet[k];
                        alphabet[k] = temps;
                    }
                }
            }
            for (int i = 0; i < 33; i++)
                chart1.Series[0].Points.AddXY(alphabet[i], N_1[i]);
        }
        // Строим график зашифрованного текста
        private void button8_Click(object sender, EventArgs e)
        {
            // Очищаем chart1
            chart2.Series[0].Points.Clear();
            string[] alphabet = { "а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я" }; // Вспомогательный буфер
            bufferOrigText = richTextBox2.Text; // Вставляем текст
            N_2 = new int[alphabet.Length]; // Массив для подсчёта частоты букв
            for (int i = 0; i < alphabet.Length; i++)
            {
                N_2[i] = 0;
                for (int j = 0; j < bufferOrigText.Length; j++)
                {
                    if (alphabet[i] == Convert.ToString(bufferOrigText[j]))
                        N_2[i]++;
                }
                // Выводим в richTextBox3
                richTextBox3.Text += " " + alphabet[i] + " " + N_2[i] + "\n";
            }
            for (int i = 0; i < alphabet.Length; i++)
            {
                for (int k = i + 1; k < alphabet.Length; k++)
                {
                    if (N_2[i] < N_2[k])
                    {
                        int temp = N_2[i];
                        N_2[i] = N_2[k];
                        N_2[k] = temp;

                        string temps = alphabet[i];//меняем буквы в алфавите в соответствии с их кол-вом
                        alphabet[i] = alphabet[k];
                        alphabet[k] = temps;
                    }
                }
            }
            for (int i = 0; i < 33; i++)
                chart2.Series[0].Points.AddXY(alphabet[i], N_2[i]);
        }
        // Расшифровка текста
        private void button4_Click(object sender, EventArgs e)
        {
            string alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"; // Вспомогательный буфер для выполнения шифра
            bool ciph; // Булевая переменная для выхода из цикла
            for (int i = 0; i < bufferOrigText.Length; i++)
            {
                ciph = true;
                for (int j = 0; j < alphabet.Length && ciph == true; j++)
                {
                    if (bufferOrigText[i] == alphabet[j])
                    {
                        bufferDecipheredText += alphabet[Math.Abs(j - n) % alphabet.Length];
                        ciph = false;
                    }
                }
            }
            richTextBox3.Text = bufferDecipheredText;
        }
    }
}
