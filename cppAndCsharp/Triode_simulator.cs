using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Simulator_triode
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        // Обработка события движения ползунка
        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            // Перезагружаем pictureBox2
            pictureBox2.Refresh();
            // Создаём новый объект графики
            Graphics g = pictureBox2.CreateGraphics();
            // Создаём карандаш
            Pen p = new Pen(Color.Black, 3);
            // Вытаскиваем значение
            int k = trackBar1.Value;
            // Недвигающаяся точка стрелки
            int start_x = pictureBox2.Width / 2, start_y = pictureBox2.Height - 10;
            int x = 15, y = 45;
            int end_x = x + k * 16, end_y1 = y - k * 4, end_y2 = 0;
            int last_k = 0;
            if (end_x < start_x)
            {
                g.DrawLine(p, start_x, start_y, end_x, end_y1);
                last_k = k;
            }
            if (end_x > start_x)
            {
                last_k = k - last_k;
                end_y2 += end_y1 + last_k * 4;
                g.DrawLine(p, start_x, start_y, end_x, end_y2);
            }
        }
    }
}
