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

namespace Vigenère_cipher
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        string cipheredText = "";
        string alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя";
        string repeat = "";
        private void button3_Click(object sender, EventArgs e)
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
        // Запуск шифрования
        private void button1_Click(object sender, EventArgs e)
        {
            string original = richTextBox1.Text.ToLower();
            writeRepeatWord(original);
            vigenereCipher(original, cipheredText, true);
        }
        // Запуск дешифрования
        private void button2_Click(object sender, EventArgs e)
        {
            repeat = "";
            cipheredText = richTextBox2.Text;
            writeRepeatWord(cipheredText);
            string decipheredText = "";
            vigenereCipher(cipheredText, decipheredText, false);
        }
        // Метод для записи повторяющегося ключа в repeat
        private void writeRepeatWord(string src)
        {
            string keyword = textBox1.Text.ToLower();
            int word_len = 0; // Для подсчёта кол-ва букв в слове
            int q = 0;
            for (int i = 0; i < src.Length + 1; i++)
                // Идем по слову пока не наткнемся на небукву
                if (i == src.Length || src[i] < 'А' || src[i] > 'я')
                {
                    for (int k = 0; k < word_len; q++, k++)
                    {
                        // По завершению слова,обнуляем q,чтобы начинать записывать с начала
                        if (q == keyword.Length)
                            q = 0;
                        repeat += keyword[q];
                    }
                    word_len = 0;
                    // Если не конец строки,то плюсуем небукву в конец слова
                    if (i != src.Length)
                        repeat += src[i];
                }
                else
                    word_len++;
        }
        // Метод,осуществляющий шифрование или дешифрование в зависимости от переменной mode
        private void vigenereCipher(string src, string dst, bool mode)
        {
            bool ciph; // булевая переменная для выхода из цикла
            for (int i = 0; i < src.Length; i++)
            {
                ciph = true;
                // Если нашли небукву,просто переносим её в ответ
                if (src[i] < 'А' || src[i] > 'я')
                    dst += src[i];
                // Иначе алгоритм Виженера
                else
                    for (int j = 0; j < alphabet.Length && ciph == true; j++)
                        if (src[i] == alphabet[j])
                            for (int q = 0; q < alphabet.Length; q++)
                                if (repeat[i] == alphabet[q])
                                {
                                    // Шифруем
                                    if (mode == true)
                                        dst += alphabet[(j + q) % alphabet.Length];
                                    // Дешифруем
                                    if (mode == false)
                                        dst += alphabet[(j + alphabet.Length - q) % alphabet.Length];
                                    ciph = false;
                                }
            }
            if (mode == true)
                richTextBox2.Text += dst;
            if (mode == false)
                richTextBox3.Text += dst;
        }
    }
}
