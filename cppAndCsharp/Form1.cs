using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace График
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        //при нажатии на кнопку выполняется этот метод/функция
        private void button1_Click(object sender, EventArgs e)
        {
            //создаем пикчербокс
            Graphics g = pictureBox1.CreateGraphics();
            //вводим коэффициент пропорциональности в окошко
            int k = int.Parse(textBox1.Text);
            //пустой массив точек,по которым будет строиться график
            PointF[] pp = new PointF[pictureBox1.Width];
            //очищаем пикчербокс
            g.Clear(pictureBox1.BackColor);
            //цикл для инициализации точек через параметрические формулы
            for (int fi = 0; fi < pictureBox1.Width; fi++)
            {
                pp[fi] = new PointF(pictureBox1.Width / 2 + (float)(k * fi * Math.PI / 180 * Math.Cos(fi * Math.PI / 180)), pictureBox1.Height / 2 + (float)(k * fi * Math.PI / 180 * Math.Sin(fi * Math.PI / 180)));
            }
            //метод,рисующий линию по массиву точек
            g.DrawLines(Pens.Black, pp);
        }
    }
}