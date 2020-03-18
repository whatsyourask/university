using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Осциллограф
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        static int n = 25;
        int[] a = new int[n];
        int j = 0; // Счётчик 

        private void button1_Click(object sender, EventArgs e)
        {
            // Заполняем массив a случайными числами
            Random rnd = new Random();
            for (int i = 0; i < n; i++)
                a[i] = rnd.Next(100);
            // Включаем timer2
            timer2.Enabled = true;
        }

        // Включает timer1
        private void timer2_Tick(object sender, EventArgs e)
        {
            timer1.Enabled = true;
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            // Заполняем listBox1
            listBox1.Items.Add("  " + j + "  " + a[j]);
            timer1.Enabled = false;
            // 
            int xk = pictureBox1.Width - 10;
            int yk = pictureBox1.Height - 15;
            // Создаём ручку и графический объект
            Pen p = new Pen(Color.Black, 3);
            Graphics g = pictureBox1.CreateGraphics();
            // Рисуем график
            g.DrawLine(p, j * 15 + 20, yk - a[j] / 2 * 5, (j + 1) * 15 + 20, yk - a[j + 1] / 2 * 5);
            j++;
            if (j == 24)
                timer2.Enabled = false;
        }

        private void button2_Click(object sender, EventArgs e)
        {
            int xk = pictureBox1.Width - 10;
            int yk = pictureBox1.Height - 15;
            // Создаём ручку и графический объект
            Pen p = new Pen(Color.Black, 3);
            Graphics g = pictureBox1.CreateGraphics();
            SolidBrush sb = new SolidBrush(Color.Black);
            // Ось y
            g.DrawLine(p, 20, 10, 20, yk);
            g.DrawLine(p, 20, 12, 25, 20);
            g.DrawLine(p, 20, 12, 15, 20);
            // Ось x
            g.DrawLine(p, 20, yk, xk, yk);
            g.DrawLine(p,xk-2,yk,xk-10,yk-5);
            g.DrawLine(p,xk-2,yk,xk-10,yk+5);
            // Рисуем штрихи по x
            for (int i = 2; i < 33; i++)
                g.DrawLine(p, 15 * i, yk - 3, 15 * i, yk + 3);
            for (int i = 1; i < 32; i += 2)
                g.DrawString(i.ToString(), this.Font, sb, 15 * i + 5, yk + 3);
            // Рисуем штрихи по y
            for (int i = 2; i < 21; i++)
                g.DrawLine(p, 16, 15 * i, 25, 15 * i);
            for (int i = 20, k = 1; i > 1; i -= 2, k += 2)
                g.DrawString(k.ToString(), this.Font, sb, 0, 15 * i - 5);
        }

        private void button3_Click(object sender, EventArgs e)
        {
            label2.Visible = true;
            label3.Visible = true;
            label4.Visible = true;
            textBox1.Visible = true;
            textBox2.Visible = true;
            textBox3.Visible = true;
            textBox1.Text = Convert.ToString(a.Average());
            textBox2.Text = Convert.ToString(a.Min());
            textBox3.Text = Convert.ToString(a.Max());
        }
    }
}
