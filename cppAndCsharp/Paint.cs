using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace lesson
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        int x_md, y_md, x_mm, y_mm; // Координаты нажатия на форме
        Color ColorPen = new Color(); // Цвет карандаша
        bool bPaint; // Флаг для контроля процесса рисования
        int pen_s; // Толщина карандаша
        int eraser_s; // Толщина ластика
        SolidBrush sb = new SolidBrush(Color.White); // Цвет ластика
        // Событие нажатия мыши
        private void Form1_MouseDown(object sender, MouseEventArgs e)
        {
            // Устанавливаем флаг активным
            bPaint = true; 
        }
        // Событие движения мыши
        private void Form1_MouseMove(object sender, MouseEventArgs e)
        {
            // Создаём объект графики для рисования
            Graphics g = CreateGraphics();
            if (bPaint)
            {
                Pen p = new Pen(ColorPen, pen_s);
                // Определяем координаты мыши при перемещении
                x_mm = e.X;
                y_mm = e.Y;
                // Рисуем
                g.DrawLine(p, x_md, y_md, x_mm, y_mm);
                // Передаем старые координаты в начало
                x_md = x_mm;
                y_md = y_mm;
                g.Dispose();
            }
            // С помощью e получаем координаты курсора 
            x_md = e.X;
            y_md = e.Y;
            // Выводим их в метки
            label1.Text = "x = " + x_md.ToString();
            label2.Text = "y = " + y_md.ToString();
        }
        // Событие отжатия мыши
        private void Form1_MouseUp(object sender, MouseEventArgs e)
        {
            // Отжали кнопку,поменяли флаг
            bPaint = false;
        }
        // Нажатие на кнопку Color
        private void button1_Click(object sender, EventArgs e)
        {
            // Открываем цвета и выбираем цвет
            colorDialog1.ShowDialog();
            ColorPen = colorDialog1.Color;
        }
        // Событие нажатия правой кнопки
        private void Form1_MouseClick(object sender, MouseEventArgs e)
        {
            // Проверяем нажата ли правая кнопка мыши
            if (e.Button == MouseButtons.Right)
            {
                // Создаём новый объект графики и очищаем
                Graphics g = CreateGraphics();
                g.Clear(this.BackColor);
                g.Dispose();
            }
        }
        // Выбираем в menuStrip 1 толщину
        private void toolStripMenuItem2_Click(object sender, EventArgs e)
        {
            pen_s = 1;
        }
        // Выбираем в menuStrip 2 толщину
        private void toolStripMenuItem3_Click(object sender, EventArgs e)
        {
            pen_s = 3;
        }
        // Выбираем в menuStrip 3 толщину
        private void toolStripMenuItem4_Click(object sender, EventArgs e)
        {
            pen_s = 6;
        }
        // Выбираем в menuStrip 4 толщину
        private void toolStripMenuItem5_Click(object sender, EventArgs e)
        {
            pen_s = 8;
        }

        private void toolStripMenuItem6_Click(object sender, EventArgs e)
        {

        }

        private void toolStripMenuItem7_Click(object sender, EventArgs e)
        {

        }

        private void toolStripMenuItem8_Click(object sender, EventArgs e)
        {

        }

        private void toolStripMenuItem9_Click(object sender, EventArgs e)
        {

        }

        // Событие движения ползунка
        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            // Устанавливаем толщину карандаша
            pen_s = trackBar1.Value;
        }
    }
}
