using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace lesson6
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            // Создаём Bitmap
            bm = new Bitmap(pictureBox1.Width, pictureBox1.Height);
            // Элементом графики станет картинка
            pictureBox1.Image = bm;
            g = Graphics.FromImage(bm);
        }
        Bitmap bm;
        Graphics g;
        int x_md, y_md, x_mm, y_mm;
        bool bPaint; // Флаг рисования(true - рисуем,false - не рисуем)
        Color cPen = Color.FromArgb(0, 0, 0); // Создаём цвет карандаша в RGB
        int pen_s; // Толщина карандаша
        // Событие нажатия мыши
        private void pictureBox1_MouseDown(object sender, MouseEventArgs e)
        {
            bPaint = true;
        }
        // Событие движения мыши
        private void pictureBox1_MouseMove(object sender, MouseEventArgs e)
        {
            if (bPaint)
            {
                Pen p = new Pen(cPen, pen_s);
                // Определяем координаты мыши при перемещении
                x_mm = e.X;
                y_mm = e.Y;
                // Рисуем
                g.DrawLine(p, x_md, y_md, x_mm, y_mm);
                // Перерисовать
                pictureBox1.Invalidate();
                // Передаем старые координаты в начало
                x_md = x_mm;
                y_md = y_mm;
            }
            // С помощью e получаем координаты курсора 
            x_md = e.X;
            y_md = e.Y;
            // Выводим их в метки
            label1.Text = "x = " + x_md.ToString();
            label2.Text = "y = " + y_md.ToString();
        }
        // Событие движения мыши
        private void pictureBox1_MouseUp(object sender, MouseEventArgs e)
        {
            bPaint = false;
        }
        // Событие нажатия правой кнопки
        private void pictureBox1_MouseClick(object sender, MouseEventArgs e)
        {

        }
        // Выбрать 1 толщину
        private void toolStripMenuItem2_Click(object sender, EventArgs e)
        {
            pen_s = 1;
        }
        // Выставляем цвет
        private void button1_Click(object sender, EventArgs e)
        {
            // Открываем цвета и выбираем цвет
            colorDialog1.ShowDialog();
            cPen = colorDialog1.Color;
        }
        // Выбираем картинку для фона pictureBox1
        private void openToolStripMenuItem_Click(object sender, EventArgs e)
        {
            OpenFileDialog dial = new OpenFileDialog();
            dial.Filter = "jpg files (*.jpg)|*.jpg|png files (*.png)|*.png|bmp files (*.bmp)|*.bmp";
            if (dial.ShowDialog() == DialogResult.OK)
            {
                bm = new Bitmap(dial.OpenFile());
                pictureBox1.Size = bm.Size;
                pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
                pictureBox1.Image = bm;
                g = Graphics.FromImage(bm);
            }
        }
        // Сохраняем
        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {
            if (pictureBox1.Image != null)
            {
                SaveFileDialog saveDial = new SaveFileDialog();
                saveDial.Filter = "jpg files (*.jpg)|*.jpg|png files (*.png)|*.png|bmp files (*bmp)|*.bmp";
                saveDial.ShowHelp = true;
                if (saveDial.ShowDialog() == DialogResult.OK)
                {
                    try
                    {
                        pictureBox1.Image.Save(saveDial.FileName);
                    }
                    catch
                    {
                        MessageBox.Show("Невозможно сохранить изображение.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
        }

        // Выбрать 2 толщину
        private void toolStripMenuItem3_Click(object sender, EventArgs e)
        {
            pen_s = 3;
        }
        // Выбрать 3 толщину
        private void toolStripMenuItem4_Click(object sender, EventArgs e)
        {
            pen_s = 6;
        }
        // Выбрать 4 толщину
        private void toolStripMenuItem5_Click(object sender, EventArgs e)
        {
            pen_s = 10;
        }
    }
}
