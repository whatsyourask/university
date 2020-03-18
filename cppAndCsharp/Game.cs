using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Тестовая_форма
{
    public partial class Dinosaurus : Form
    {
        // Создаём глобальное все объекты нужных классов
        Graphics gr;
        Bitmap MyBitm;
        Random r = new Random();
        Pen p = new Pen(Color.Black, 2.5f);
        Pen pw = new Pen(Color.White, 2.5f);
        SolidBrush sb1, sb2;
        // Инициализируем глобально необходимые переменные
        int MovX = 992, MovY = 360;
        int mode1 = 0; // Переменная для случайной генерации кочек на земле
        int mode2 = 0; // Переменная для случайной генерации облаков
        // x1-x4 - переменные для генерации полосок на земле
        int x1 = 1553;
        int x2 = 1503;
        int x3 = 1453;
        int x4 = 1403;
        int y = 363;
        // Начальные координаты облаков
        int cloud_x1 = 2000;
        int cloud_y1 = 100;
        // Начальные координаты кактусов(препятствий)
        int obst_x = 1100;
        int del1; // Разница в координатах Х генерируемых препятствий
        // Начальные координаты орлов
        int eagle_x = 1100, eagle_y = 160;
        int del2; // Разница в координатах Х генерируемых орлов
        bool down = false; // Логическая переменная,отвечающая за движение персонажа вертикально(true - если вниз)
        // passed1 - отвечает за преодоление препятствий(кактусов), passed2 - отвечает за начисление очков в счётчик
        // passed3 - отвечает за преодоление препятствий(орлов),color - отвечает за инверсию(если true - делается инверсия цвета)
        bool passed1 = true, passed2, passed3 = true, color = false;
        // Точки,относительно которых оценивается столкновение персонажа с препятствиями
        int front_obst_x1, front_obst_y1=280;
        int front_liz1_x1, front_liz1_y1;
        // Переменная для счётчика
        int sum = 0;
        // Переменные,для ускорения в процессе набора очков
        int diff = 4, diff_eagle = 6, diff_cloud = 2;
        // Координаты персонажа
        int liz_x = 245, liz_y = 330;
        // Переменная,отвечающая за нажатие клавиши "пробел"
        bool keyup = false;
        public Dinosaurus()
        {
            InitializeComponent();
            //this.WindowState = FormWindowState.Maximized;
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            // Убираем кнопки свернуть, развернуть, закрыть.
            this.ControlBox = false;
            // Убираем заголовок.
            this.Text = "";
            this.FormBorderStyle = FormBorderStyle.None;
        }
        // Нажимаем на "Начать"
        private void button1_MouseClick(object sender, MouseEventArgs e)
        {
            MyBitm = new Bitmap(pictureBox4.Width, pictureBox4.Height);
            gr = Graphics.FromImage(MyBitm);
            // Инициализируем SolidBrush
            sb1 = new SolidBrush(Color.White);
            sb2 = new SolidBrush(Color.Black);
            // Включаем SmoothingMode
            gr.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
            // Закрашиваем весь фон
            gr.FillRectangle(sb1, 0, 0, pictureBox4.Width, pictureBox4.Height);
            // Рисуем землю
            Ground(0, 0, 0);
            // Рисуем персонажа
            lizard(liz_x, liz_y);
            pictureBox4.Image = MyBitm;
            // Включаем таймер
            timer1.Enabled = true;
            // Убираем все кнопки и метки
            button1.Visible = false;
            button2.Visible = false;
            label1.Visible = true;
        }
        // Нажимаем "Выход"
        private void button2_MouseClick(object sender, MouseEventArgs e)
        {
            // Закрываем программу
            this.Close();
        }
        // Назначаем на клавишу обработку
        protected override bool ProcessCmdKey(ref Message msg, Keys keyData)
        {
            // Если нажата клавиша "пробел" и координата Y персонажа начальная и до этого не нажимали клавишу(т.е. keyup == false)
            if (keyData == Keys.Space && liz_y == 330 && keyup == false)
            {
                keyup = true;
                return true;
            }
            return base.ProcessCmdKey(ref msg, keyData);
        }
        private void timer1_Tick(object sender, EventArgs e)
        {
            //В зависимости от переменной цвета будет рисоваться тот или иной цвет
            if (color)
                gr.FillRectangle(sb2, 0, 0, pictureBox4.Width, pictureBox4.Height);
            else
                gr.FillRectangle(sb1, 0, 0, pictureBox4.Width, pictureBox4.Height);
            timer1.Interval = 1;
            // Двигаем землю с кочками влево
            Ground(MovX, MovY, mode1);
            MovX -= diff;
            //Если дошли до определённых координат,то сбрасываем их и меняем мод
            if (MovX < 213)
            {
                MovX = 992;
                mode1 = r.Next(0, 3);
            }
            // Рисуем полоски на земле,чтобы придать ей движение
            lines1(x1, y);
            lines1(x2, y + 2);
            lines1(x3, y + 5);
            lines1(x4, y - 3);
            // Смещаем координаты полосок
            x1 -= diff;
            x2 -= diff;
            x3 -= diff;
            x4 -= diff;
            // Сбрасываем координаты по достижению определённых координат
            if (x1 < 100)
                x1 = 1053;
            if (x2 < 100)
                x2 = 1003;
            if (x3 < 100)
                x3 = 953;
            if (x4 < 100)
                x4 = 903;
            // Рисуем облака
            cloud(cloud_x1, cloud_y1, mode2);
            // Смещаем координаты облаков
            cloud_x1 -= diff_cloud;
            // Сбрасываем координаты по достижению определёных координат и меняем мод
            if (cloud_x1 < 20)
            {
                mode2 = r.Next(0, 3);
                cloud_x1 = 2000;
            }
            // Рисуем препятствие
            obstacles(obst_x);
            // Смещаем препятствие
            obst_x -= diff;
            // Сбрасываем препятствие и немного изменяем координаты X его генерации
            if (obst_x < 120)
            {
                del1 = r.Next(0, 50);
                obst_x = 1100 + del1;
                // Если игрок перепрыгнул,то делаем passed2 = true,т.е. +1 очко
                if (passed1)
                {
                    passed2 = true;
                }
            }
            // Перерисовываем персонажа
            lizard(liz_x, liz_y);
            // Смещаем точки,тносительно которых оценивается преодоление препятствия
            front_obst_x1 = obst_x - 27;
            front_liz1_x1 = liz_x + 155;
            front_liz1_y1 = liz_y + 45;
            // Если клавиша нажата,то поднимаем рисунок персонажа вверх
            if (keyup == true)
                liz_y -= 4;
            // При достижении определённых координат,ставим down = true и нажатие клавиши в false
            if (liz_y < 150)
            {
                down = true;
                keyup = false;
            }
            // Если down == true,значит персонаж должен опускаться,опускаем
            if (down)
                liz_y += 3;
            // Сбрасываем координаты и помечаем в down,что персонаж опустился
            if (liz_y > 330)
            {
                down = false;
                liz_y = 330;
            }
            // При достижении этих диапазонов очков в игру вступают орлы
            if ((sum > 50 && sum < 100) || (sum > 150 && sum < 200))
            {
                // Рисуем орла
                eagle(eagle_x, eagle_y);
                // Смещаем орла
                eagle_x -= diff_eagle;
                // Сбрасываем его координаты в начало
                if (eagle_x < 50)
                {
                    // С помощью del2 изменяем начальные координаты генерации
                    del2 = r.Next(100, 500);
                    eagle_x = 1100 + del2;
                    // Если игрок не задел орла,то делаем passed2 в true,т.е. +1 очко
                    if (passed3)
                    {
                        passed2 = true;
                    }
                }
                // Оцениваем расстояние между точками,чтобы понять:преодолел персонаж препятствие или нет(дя орлов)
                if (front_liz1_y1 - eagle_y < 100 &&  Math.Abs(front_liz1_x1 - eagle_x) < 240)
                {
                    // Если не преодолел,останавливаем таймер и завершаем игру всплывающим окном
                    timer1.Stop();
                    passed3 = false;
                    // Вызов окна
                    show_message(sum);
                }
            }
            // Аналогично,только для препятствий
            if (front_obst_x1 < front_liz1_x1 && front_obst_y1 < front_liz1_y1 && front_liz1_x1 - front_obst_x1 < 170)
            {
                timer1.Stop();
                passed1 = false;
                show_message(sum);
            }
            // Если персонаж преодолел препятствие
            if (passed2)
            {
                // Добавляем очко
                sum++;
                // Обновляем счётчик
                label1.Text = Convert.ToString(sum);
                // Возвращаем переменную в false
                passed2 = false;
                // Смотрим на его кол-во набранных очков,если они кратны 10 и не 0,ускоряем игру
                if (sum % 10 == 0 && sum != 0)
                {
                    diff++;
                    // Для придачи эффекта,ускоряем и облака
                    diff_cloud++;
                }
                // Когда очки перевалят за 50,ускоряем и орлов
                if (sum % 10 == 0 && sum > 50)
                    diff_eagle++;
                // При достижении этих диапазонов очков в игре происходит инверсия цвета
                if (sum > 50 && sum < 100 || sum > 150 && sum < 200)
                {
                    color = true;
                    // Меняем цвета пикчербоксов
                    pictureBox2.BackColor = Color.Black;
                    pictureBox3.BackColor = Color.Black;
                    // Меняем цвета счётчика
                    label1.BackColor = Color.Black;
                    label1.ForeColor = Color.White;
                }
                else
                {
                    color = false;
                }
            }
            pictureBox4.Image = MyBitm;
        }
        // Функция рисования дороги
        private void Ground(int x1, int y1, int mode)
        {   
            //4 варианта рисования кочек на дороге
            if (x1 == 0 && y1 == 0 && mode == 0)
            {
                Point[] ground = { new Point(213, 360), new Point(1053, 360) };
                if (color)
                    gr.DrawLines(pw, ground);
                else
                    gr.DrawLines(p, ground);
            }
            else if (mode == 1)
            {
                int x2 = x1 + 12, y2 = 354;
                int x3 = x2 + 16, y3 = 352;
                int x4 = x3 + 26, y4 = 355;
                int x5 = x4 + 10, y5 = 360;
                Point[] ground = { new Point(213, 360), new Point(x1, y1), new Point(x2, y2), new Point(x3, y3), new Point(x4, y4), new Point(x5, y5), new Point(1053, 360) };
                if (color)
                    gr.DrawLines(pw, ground);
                else
                    gr.DrawLines(p, ground);
            }
            else if (mode == 2)
            {
                int x2 = x1 + 15, y2 = 356;
                int x3 = x2 + 20, y3 = 354;
                int x4 = x3 + 22, y4 = 358;
                int x5 = x4 + 25, y5 = 360;
                Point[] ground = { new Point(213, 360), new Point(x1, y1), new Point(x2, y2), new Point(x3, y3), new Point(x4, y4), new Point(x5, y5), new Point(1053, 360) };
                if (color)
                    gr.DrawLines(pw, ground);
                else
                    gr.DrawLines(p, ground);
            }
            else
            {
                int x2 = x1 + 12, y2 = 355;
                int x3 = x2 + 18, y3 = 357;
                int x4 = x3 + 22, y4 = 356;
                int x5 = x4 + 15, y5 = 360;
                Point[] ground = { new Point(213, 360), new Point(x1, y1), new Point(x2, y2), new Point(x3, y3), new Point(x4, y4), new Point(x5, y5), new Point(1053, 360) };
                if (color)
                    gr.DrawLines(pw, ground);
                else
                    gr.DrawLines(p, ground);
            }
        }
        // Функция рисования полосок на дороге
        private void lines1(int x, int y)
        {
            int len1 = 5, len2 = 7, len3 = 3, len4 = 9;
            if (color) {
                gr.DrawLine(pw, new Point(x, y + 12), new Point(x + len2, y + 12));
                x += 50;
                gr.DrawLine(pw, new Point(x, y + 7), new Point(x + len1, y + 7));
                x += 50;
                gr.DrawLine(pw, new Point(x, y + 11), new Point(x + len4, y + 11));
                x += 50;
                gr.DrawLine(pw, new Point(x, y + 20), new Point(x + len3, y + 20));
                x += 50;
                gr.DrawLine(pw, new Point(x, y + 13), new Point(x + len4, y + 13));
                x += 50;
                gr.DrawLine(pw, new Point(x, y + 25), new Point(x + len4, y + 25));
                x += 50;
                gr.DrawLine(pw, new Point(x, y + 19), new Point(x + len4, y + 19));
                x += 50;
                gr.DrawLine(pw, new Point(x, y + 15), new Point(x + len4, y + 15));
            }
            else
            {
                gr.DrawLine(p, new Point(x, y + 12), new Point(x + len2, y + 12));
                x += 50;
                gr.DrawLine(p, new Point(x, y + 7), new Point(x + len1, y + 7));
                x += 50;
                gr.DrawLine(p, new Point(x, y + 11), new Point(x + len4, y + 11));
                x += 50;
                gr.DrawLine(p, new Point(x, y + 20), new Point(x + len3, y + 20));
                x += 50;
                gr.DrawLine(p, new Point(x, y + 13), new Point(x + len4, y + 13));
                x += 50;
                gr.DrawLine(p, new Point(x, y + 25), new Point(x + len4, y + 25));
                x += 50;
                gr.DrawLine(p, new Point(x, y + 19), new Point(x + len4, y + 19));
                x += 50;
                gr.DrawLine(p, new Point(x, y + 15), new Point(x + len4, y + 15));
            }
        }
        // Функция рисования облаков
        private void cloud(int x, int y, int mode)
        {
            // 3 варианта рисования облаков
            if (mode == 0)
            {
                Point[] clouds1 = { new Point(x,y),new Point(x-80,y), new Point(x-90,y-10)
            ,new Point(x-80,y-20),new Point(x-60,y-30),new Point(x-40,y-25)
            ,new Point(x-10,y-35),new Point(x+10,y-15),new Point(x+15,y-5),new Point(x,y)};
                Pen gray_p = new Pen(Color.Gray, 2.5f);
                gr.DrawCurve(gray_p, clouds1);
                x -= 200;
                y += 100;
                Point[] clouds2 = { new Point(x,y),new Point(x-80,y), new Point(x-90,y-10)
            ,new Point(x-80,y-20),new Point(x-60,y-30),new Point(x-40,y-25)
            ,new Point(x-10,y-35),new Point(x+10,y-15),new Point(x+15,y-5),new Point(x,y)};
                gr.DrawCurve(gray_p, clouds2);
                x -= 150;
                y -= 150;
                Point[] clouds3 = { new Point(x,y),new Point(x-80,y), new Point(x-90,y-10)
            ,new Point(x-80,y-20),new Point(x-60,y-30),new Point(x-40,y-25)
            ,new Point(x-10,y-35),new Point(x+10,y-15),new Point(x+15,y-5),new Point(x,y)};
                gr.DrawCurve(gray_p, clouds3);
            }
            else if (mode == 1)
            {
                Point[] clouds1 = { new Point(x,y),new Point(x-80,y), new Point(x-90,y-10)
            ,new Point(x-80,y-20),new Point(x-60,y-30),new Point(x-40,y-25)
            ,new Point(x-10,y-35),new Point(x+10,y-15),new Point(x+15,y-5),new Point(x,y)};
                Pen gray_p = new Pen(Color.Gray, 2.5f);
                gr.DrawCurve(gray_p, clouds1);
                x -= 150;
                y -= 25;
                Point[] clouds2 = { new Point(x,y),new Point(x-80,y), new Point(x-90,y-10)
            ,new Point(x-80,y-20),new Point(x-60,y-30),new Point(x-40,y-25)
            ,new Point(x-10,y-35),new Point(x+10,y-15),new Point(x+15,y-5),new Point(x,y)};
                gr.DrawCurve(gray_p, clouds2);
                x -= 100;
                y += 125;
                Point[] clouds3 = { new Point(x,y),new Point(x-80,y), new Point(x-90,y-10)
            ,new Point(x-80,y-20),new Point(x-60,y-30),new Point(x-40,y-25)
            ,new Point(x-10,y-35),new Point(x+10,y-15),new Point(x+15,y-5),new Point(x,y)};
                gr.DrawCurve(gray_p, clouds3);
            }
            else
            {
                Point[] clouds1 = { new Point(x,y),new Point(x-80,y), new Point(x-90,y-10)
            ,new Point(x-80,y-20),new Point(x-60,y-30),new Point(x-40,y-25)
            ,new Point(x-10,y-35),new Point(x+10,y-15),new Point(x+15,y-5),new Point(x,y)};
                Pen gray_p = new Pen(Color.Gray, 2.5f);
                gr.DrawCurve(gray_p, clouds1);
                x -= 50;
                y -= 75;
                Point[] clouds2 = { new Point(x,y),new Point(x-80,y), new Point(x-90,y-10)
            ,new Point(x-80,y-20),new Point(x-60,y-30),new Point(x-40,y-25)
            ,new Point(x-10,y-35),new Point(x+10,y-15),new Point(x+15,y-5),new Point(x,y)};
                gr.DrawCurve(gray_p, clouds2);
                x += 150;
                y += 150;
                Point[] clouds3 = { new Point(x,y),new Point(x-80,y), new Point(x-90,y-10)
            ,new Point(x-80,y-20),new Point(x-60,y-30),new Point(x-40,y-25)
            ,new Point(x-10,y-35),new Point(x+10,y-15),new Point(x+15,y-5),new Point(x,y)};
                gr.DrawCurve(gray_p, clouds3);
            }
        }   
        // Функция рисования препятствия
        private void obstacles(int x)
        {
            Point[] obstac = { new Point(x+18,315), new Point(x+14,325), new Point(x+9,315),
            new Point(x+9,270),new Point(x+2,260),new Point(x-5,270),
            new Point(x-5,310),new Point(x-10,320),new Point(x-15,310),
            new Point(x-15,290),new Point(x-21,280),new Point(x-27,290),
            new Point(x-27,325),new Point(x-19,335),
            new Point(x-8,335),new Point(x-8,365),
            new Point(x,369),new Point(x+8,365),
            new Point(x+8,335),new Point(x+19,335),
            new Point(x+27,325),new Point(x+27,300),new Point(x+23,290),
            new Point(x+19,300),new Point(x+18,315)};
            if (color)
                gr.FillClosedCurve(Brushes.White, obstac);
            else
                gr.FillClosedCurve(Brushes.Black, obstac);
        }
        // Функция рисования орлов
        private void eagle(int x,int y)
        {
            // x == 253; y = 410
            Point[] eagle1 = { new Point(x, y),new Point(x+1,y-9), new Point(x+9,y-14),new Point(x+20,y-18),new Point(x+41,y-22),new Point(x+43,y-40),
            new Point(x+42,y-45),new Point(x+33,y-57),new Point(x+22,y-68),new Point(x+16,y-73),new Point(x+12,y-76),new Point(x+10,y-80),
            new Point(x+16,y-86),new Point(x+20,y-88),new Point(x+45,y-88),new Point(x+64,y-84),new Point(x+77,y-96),new Point(x+88,y-96),
            new Point(x+116,y-98),new Point(x+134,y-99),new Point(x+160,y-92),new Point(x+179,y-86),new Point(x+202,y-77),new Point(x+207,y-72),
            new Point(x+211,y-66),new Point(x+197,y-62),new Point(x+181,y-64),new Point(x+174,y-24),new Point(x+176,y-48),new Point(x+169,y-39),
            new Point(x+168,y-29),new Point(x+158,y-14),new Point(x+140,y-10),new Point(x+148,y-4),new Point(x+154,y-4),new Point(x+162,y-4),
            new Point(x+176,y-2),new Point(x+184,y+3),new Point(x+178,y+8),new Point(x+163,y+7),new Point(x+156, y+2),new Point(x+153,y+11),
            new Point(x+140,y+12),new Point(x+129,y+12),new Point(x+112,y+10),new Point(x+98,y+14),new Point(x+90,y+17),new Point(x+80,y+16),
            new Point(x+68,y+14),new Point(x+59,y+10),new Point(x+47,y+8),new Point(x+40,y+8),new Point(x+22,y+3),new Point(x+14,y-2),
            new Point(x+10,y-5),new Point(x+5,y-4),new Point(x,y) };
            if (color)
            {
                gr.FillClosedCurve(Brushes.White, eagle1);
                gr.DrawClosedCurve(pw, eagle1);
                gr.FillRectangle(Brushes.Black, x + 18, y - 12, 4, 4);
            }
            else {
                gr.FillClosedCurve(Brushes.Black, eagle1);
                gr.DrawClosedCurve(p, eagle1);
                gr.FillRectangle(Brushes.White, x + 18, y - 12, 4, 4);
            }
        }
        // Функция рисования персонажа
        private void lizard(int x, int y)
        {
            // x = 245 y = 330
            Point[] lizard = {
            new Point(x,y), new Point(x+15,y+4), new Point(x+37,y+7), new Point(x+47,y+7), new Point(x+53,y+6),
            new Point(x+49,y+14),new Point(x+43,y+22),new Point(x+41,y+26),new Point(x+39,y+33),new Point(x+40,y+39),
            new Point(x+59,y+40),new Point(x+40,y+39),new Point(x+49,y+23),new Point(x+56,y+15),new Point(x+67,y+8),
            new Point(x+77,y+4),new Point(x+94,y+6),new Point(x+104,y+18),new Point(x+107,y+18),new Point(x+115,y+36),
            new Point(x+130,y+43),new Point(x+143,y+44),new Point(x+153,y+43),new Point(x+135,y+40),new Point(x+125,y+34),
            new Point(x+118,y+27),new Point(x+113,y+12),new Point(x+95,y-6),new Point(x+93,y-10),new Point(x+103,y-15),
            new Point(x+110,y-21),new Point(x+121,y-19),new Point(x+129,y-18),new Point(x+129,y-24),new Point(x+133,y-26),
            new Point(x+139,y-26),new Point(x+134,y-28),new Point(x+128,y-26),new Point(x+123,y-23),new Point(x+115,y-25),
            new Point(x+115,y-31),new Point(x+121,y-37),new Point(x+137,y-36),new Point(x+143,y-35),new Point(x+152,y-35),
            new Point(x+147,y-37),new Point(x+134,y-40),new Point(x+125,y-40),new Point(x+118,y-42),new Point(x+121,y-54),
            new Point(x+127,y-60),new Point(x+135,y-66),new Point(x+142,y-69),new Point(x+134,y-71),new Point(x+118,y-71),
            new Point(x+110,y-71),new Point(x+99,y-66),new Point(x+93,y-55),new Point(x+101,y-54),new Point(x+105,y-53),
            new Point(x+106,y-50),new Point(x+106,y-46),new Point(x+92,y-36),new Point(x+82,y-24),new Point(x+64,y-11),
            new Point(x+37,y-1),new Point(x+21,y-2),new Point(x+8,y-2),new Point(x,y)
            };
            if (color)
            {
                gr.FillClosedCurve(Brushes.White, lizard);
                gr.FillRectangle(Brushes.Black, x + 117, y - 65, 3, 3);
                gr.DrawClosedCurve(pw, lizard);
            }
            else
            {
                gr.FillClosedCurve(Brushes.Black, lizard);
                gr.FillRectangle(Brushes.White, x + 117, y - 65, 3, 3);
                gr.DrawClosedCurve(p, lizard);
            }
            
        }
        // функция отправки всплывающего окна
        private void show_message(int sum)
        {
            // Строка "Ваши очки: "
            string message = "Your points:" + sum;
            // Название окна
            string title = "End game";
            // Создаем объект MessageBoxButtons с кнопками повторить и отмена
            MessageBoxButtons buttons = MessageBoxButtons.RetryCancel;
            DialogResult dr = MessageBox.Show(message,title,buttons);
            if (dr == DialogResult.Retry)
            {
                reset();
            }
            else
            {
                this.Close();
            }
        }
        // С помощью этой функции возвращаем все переменные в начальное состояние
        private void reset()
        {
            MovX = 992;
            MovY = 360;
            mode1 = 0;
            mode2 = 0;
            x1 = 1553;
            x2 = 1503;
            x3 = 1453;
            x4 = 1403;
            y = 363;
            cloud_x1 = 2000;
            cloud_y1 = 100;
            obst_x = 1100;
            eagle_x = 1100;
            eagle_y = 160;
            down = false;
            passed1 = true;
            passed3 = true;
            color = false;
            front_obst_y1 = 280;
            sum = 0;
            label1.Text = Convert.ToString(sum);
            diff = 4;
            diff_eagle = 6;
            diff_cloud = 2;
            liz_x = 245;
            liz_y = 330;
            keyup = false;
            pictureBox2.BackColor = Color.White;
            pictureBox3.BackColor = Color.White;
            label1.BackColor = Color.White;
            label1.ForeColor = Color.Black;
            gr.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
            gr.FillRectangle(sb1, 0, 0, pictureBox4.Width, pictureBox4.Height);
            Ground(0, 0, 0);
            lizard(liz_x, liz_y);
            pictureBox4.Image = MyBitm;
            timer1.Start();
        }
    }
}
