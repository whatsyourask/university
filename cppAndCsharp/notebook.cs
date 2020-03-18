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

namespace notebook
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        //Переменная для текста
        string BufferText = "";
        // Метод для Copy(Edit)
        private void toolStripMenuItem12_Click(object sender, EventArgs e)
        {
            BufferText = richTextBox2.SelectedText;
        }
        // Метод для Cut(Edit)
        private void toolStripMenuItem7_Click(object sender, EventArgs e)
        {
            BufferText = richTextBox2.SelectedText;
            richTextBox2.SelectedText = "";
        }
        // Метод для Paste(Edit)
        private void toolStripMenuItem6_Click(object sender, EventArgs e)
        {
            richTextBox2.SelectedText = BufferText;
        }
        // Метод для Size(Font)
        private void toolStripMenuItem9_Click(object sender, EventArgs e)
        {
            // Делаем label3 и comboBox3 видимыми
            label3.Visible = true;
            comboBox3.Visible = true;
        }
        // Метод для изменения размера шрифта через comboBox3
        private void comboBox3_SelectedIndexChanged(object sender, EventArgs e)
        {
            richTextBox2.SelectionFont = new Font(richTextBox2.Font.FontFamily, Convert.ToInt32(comboBox3.Text));
        }
        // Метод для Color(Font)
        private void toolStripMenuItem10_Click(object sender, EventArgs e)
        {
            if (colorDialog1.ShowDialog() == DialogResult.OK)
                richTextBox2.SelectionColor = colorDialog1.Color;
        }
        // Метод для Type(Font)
        private void toolStripMenuItem11_Click(object sender, EventArgs e)
        {
            // Делаем label4 и comboBox4 видимыми
            label4.Visible = true;
            comboBox4.Visible = true;
        }
        // Метод для изменения типа шрифта через ComboBox4
        private void comboBox4_SelectedIndexChanged(object sender, EventArgs e)
        {
            // Переменная для запоминания выбранного типа шрифта
            string Font = "";
            // Копируем из comboBox4.Text в Font
            Font = comboBox4.Text;
            // Сравниваем
            if (Font == "Bold")
                richTextBox2.SelectionFont = new Font(richTextBox2.Font.FontFamily, this.Font.Size, FontStyle.Bold);
            if (Font == "Italic")
                richTextBox2.SelectionFont = new Font(richTextBox2.Font.FontFamily, this.Font.Size, FontStyle.Italic);
            if (Font == "Underline")
                richTextBox2.SelectionFont = new Font(richTextBox2.Font.FontFamily, this.Font.Size, FontStyle.Underline);
        }
        // Метод для открытия файла
        private void toolStripMenuItem3_Click(object sender, EventArgs e)
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
                    // Считываем в richTextBox2
                    richTextBox2.Text = streamreader.ReadToEnd();
                    // Закрываем поток
                    filestream.Close();
                }
            }
        }
        // Метод для сохранения файла
        private void siteToolStripMenuItem_Click(object sender, EventArgs e)
        {
            saveFileDialog1.Filter = "txt files(*.txt|*.txt|All files (*.*)|*.*)";
            if (saveFileDialog1.ShowDialog() == DialogResult.OK)
            {
                // Копируем имя
                string fileName = saveFileDialog1.FileName;
                // Создаём объект класса Filestream(для управления потоком)
                FileStream filestream = File.Open(fileName, FileMode.Create, FileAccess.Write);
                // Если что-то есть в потоке,то выполняем блок
                if (filestream != null)
                {
                    // Создаём объект класса StreamWriter для сохранения
                    StreamWriter streamwriter = new StreamWriter(filestream);
                    // Записываем через streamwriter
                    streamwriter.Write(richTextBox2.Text);
                    streamwriter.Flush();
                    // Закрываем поток
                    filestream.Close();
                }
            }
        }
    }
}
