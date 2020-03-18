using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Рик_в_пикчербоксе
{
    public partial class RickAnimation : Form
    {
        Graphics gr;
        Pen p = new Pen(Color.Black, 2.5f);
        Bitmap MyBitm;
        public RickAnimation()
        {
            InitializeComponent();
        }
        int x = 95; // смещение глаза вправо
        private void PictureBox(object sender,EventArgs e)
        {
            MyBitm = new Bitmap(pictureBox1.Width, pictureBox1.Height);
            gr = Graphics.FromImage(MyBitm);
            gr.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
            //gr = pictureBox1.CreateGraphics();
            Paint_Rick();
            pictureBox1.Image = MyBitm;
            timer1.Enabled = true;
        }
        int MovX = 220, MovY = 183;
        private void timer1_Tick(object sender, EventArgs e)
        {
            Mouth_Paint();
            timer1.Interval = 50;
            Eyes_Paint();
            Pupils_Paint(MovX, MovY);
            MovX -= 5;
            MovY += 1;
            if (MovX < 190)
            {
                timer1.Stop();
                // Другое действие
                Paint_Rick();
                Pupils_Paint(MovX, MovY);
                Mouth_Paint2();
                MovX = 220; 
                MovY = 183;
            }
            pictureBox1.Image = MyBitm;
        }
        void Paint_Rick() {
            Hair_Paint();
            Robe_Paint();
            T_shirt_Paint();
            Neck_Paint();
            Head_Paint();
            Eyes_Paint();
            Nose_Paint();
            Brow_Paint();
            Ears_Paint();
        }
        void Head_Paint()
        {
            // Массив точек для головы
            Point[] head = { new Point(240, 72), new Point(210, 75), new Point(180, 90), new Point(147, 130), new Point(133, 228),
                new Point(160, 333), new Point(240, 374), new Point(317, 329), new Point(332, 220),
                new Point(322, 132), new Point(300, 95), new Point(272, 76),new Point(240, 72) };
            // Рисуем замкнутую закрашенную кривую
            gr.FillClosedCurve(Brushes.LightGray, head);
            // Обводка
            gr.DrawCurve(p, head);
        }
        void Eyes_Paint()
        {
            // Массив точек для 1 глаза
            Point[] eye_one = { new Point(185, 157),new Point(173,167),new Point(165, 190), new Point(182, 220), new Point(222, 225),
                new Point(244,209),new Point(248, 185),new Point(245, 170),new Point(232, 158)};
            // Рисуем незамкнутую закрашенную кривую
            gr.FillClosedCurve(Brushes.LightGray, eye_one);
            // Обводка
            gr.DrawCurve(p, eye_one);

            
            // Массив точек для 2 глаза
            Point[] eye_two = { new Point(185+x, 157),new Point(173+x,167),new Point(165+x, 185), new Point(182+x, 220), new Point(222+x, 225),
                new Point(244+x,209),new Point(248+x, 185),new Point(245+x, 170),new Point(229+x, 155)};
            // Рисуем незамкнутую закрашенную кривую
            gr.FillClosedCurve(Brushes.LightGray, eye_two);
            // Обводка
            gr.DrawCurve(p, eye_two);

            // Массив точек для 1 глаза(Заполнение белым)
            Point[] white_eye_one = {new Point(165+46,185),new Point(165+45,185),new Point(165+40,186),new Point(165, 188), new Point(182, 220), new Point(222, 225),
                new Point(244,209),new Point(248,186),new Point(248, 185),new Point(245, 185),new Point(165+46,185)};
            // Рисуем незамкнутую закрашенную кривую
            gr.FillClosedCurve(Brushes.White, white_eye_one);
            // Обводка
            gr.DrawClosedCurve(p, white_eye_one);

            // Массив точек для 2 глаза(Заполнение белым)
            Point[] white_eye_two = {new Point(165+46+x,185),new Point(165+45+x,185),new Point(165+40+x,186),new Point(165+x, 188), new Point(182+x, 220), new Point(222+x, 225),
                new Point(244+x,209),new Point(248+x,186),new Point(248+x, 185),new Point(245+x, 185),new Point(165+46+x,185)};
            // Рисуем незамкнутую закрашенную кривую
            gr.FillClosedCurve(Brushes.White, white_eye_two);
            // Обводка
            gr.DrawClosedCurve(p, white_eye_two);

            //// Рисуем зрачки
            //gr.FillEllipse(Brushes.Black, 220, 183, 13, 13);
            //gr.FillEllipse(Brushes.Black, 220 + x, 183, 13, 13);

            // Массив точек для левого мешка под глазом
            Point[] bag_left = { new Point(166, 229), new Point(174, 237), new Point(190, 243), new Point(216, 240) };
            // Рисуем кривую линию
            gr.DrawCurve(p, bag_left);

            // Массив точек для правого мешка под глазом
            Point[] bag_right = { new Point(288, 239), new Point(304, 241), new Point(318, 239), new Point(331, 229), new Point(334, 220) };
            // Рисуем незамкнутую закрашенную кривую
            gr.FillClosedCurve(Brushes.LightGray, bag_right);
            // Рисуем обводку кривой
            gr.DrawCurve(p, bag_right);
        }
        void Pupils_Paint(int x1,int y1)
        {
            // Рисуем зрачки
            gr.FillEllipse(Brushes.Black, x1, y1, 13, 13);
            gr.FillEllipse(Brushes.Black, x1 + x, y1, 13, 13);
        }
        //void Half_Eyes_Paint()
        //{
        //    // Массив точек для 1 глаза
        //    Point[] eye_one1 = { new Point(185, 157), new Point(173, 167), new Point(165, 190), new Point(182, 220) };
        //    Point[] eye_one2 = { new Point(222, 225),
        //        new Point(244,209),new Point(248, 185),new Point(245, 170),new Point(230, 159)};
        //    // Рисуем незамкнутую закрашенную кривую
        //    gr.FillClosedCurve(Brushes.LightGray, eye_one1);
        //    gr.FillClosedCurve(Brushes.LightGray, eye_one2);
        //    // Обводка
        //    Point[] eye_one2_double = { new Point(222, 225),
        //        new Point(244,209),new Point(248, 185),new Point(245, 170),new Point(230, 155)};
        //    gr.DrawCurve(p, eye_one1);
        //    gr.DrawCurve(p, eye_one2_double);

        //    // Массив точек для 2 глаза
        //    Point[] eye_two1 = { new Point(185 + x, 157), new Point(173 + x, 167), new Point(165 + x, 190), new Point(182 + x, 220) };
        //    Point[] eye_two2 = { new Point(222+x, 225),
        //        new Point(244+x,209),new Point(248+x, 185),new Point(245+x, 170),new Point(230+x, 159)};
        //    // Рисуем незамкнутую закрашенную кривую
        //    gr.FillClosedCurve(Brushes.LightGray, eye_two1);
        //    gr.FillClosedCurve(Brushes.LightGray, eye_two2);
        //    // Обводка
        //    Point[] eye_two2_double = { new Point(222+x, 225),
        //        new Point(244+x,209),new Point(248+x, 185),new Point(245+x, 170),new Point(230+x, 155)};
        //    gr.DrawCurve(p, eye_two1);
        //    gr.DrawCurve(p, eye_two2_double);

        //    // Массив точек для 1 глаза(Заполнение белым)
        //    Point[] white_eye_one = {new Point(165+46,185),new Point(165+45,185),new Point(165+40,186),new Point(165, 188), new Point(182, 220), new Point(222, 225),
        //        new Point(244,209),new Point(248,186),new Point(248, 185),new Point(245, 185),new Point(165+46,185)};
        //    // Рисуем незамкнутую закрашенную кривую
        //    gr.FillClosedCurve(Brushes.White, white_eye_one);
        //    // Обводка
        //    Point[] one = {new Point(165 + 45, 185), new Point(165 + 40, 185), new Point(245, 185), new Point(248, 186) };
        //    gr.DrawCurve(p,one);

        //    // Массив точек для 2 глаза(Заполнение белым)
        //    Point[] white_eye_two = {new Point(165+46+x,185),new Point(165+45+x,185),new Point(165+40+x,186),new Point(165+x, 188),
        //        new Point(248+x,186),new Point(248+x, 185),new Point(245+x, 185)};
        //    // Рисуем незамкнутую закрашенную кривую
        //    gr.FillClosedCurve(Brushes.White, white_eye_two);
        //    // Обводка
        //    Point[] two = { new Point(248+x, 186), new Point(245+x, 185), new Point(165 + 45+x, 185), new Point(165 + 40+x, 185) };
        //    gr.DrawCurve(p, two);
        //}
        void Nose_Paint()
        {
            // Массив точек для носа
            Point[] nose_points = { new Point(249, 238), new Point(257, 255), new Point(271, 268), new Point(277, 253), new Point(277, 241), new Point(272, 221) };
            // Рисуем кривую
            gr.DrawCurve(p, nose_points);
        }
        void Brow_Paint()
        {
            // Массив точек для брови
            Point[] Brow = { new Point(186,132),new Point(183,136),new Point(184, 142), new Point(190, 143) , new Point(221, 129) , new Point(259, 121) , new Point(298, 129) , new Point(319, 138),
            new Point(325, 136),new Point(319, 124),new Point(295, 111),new Point(259, 106),new Point(221, 112),new Point(190, 127),new Point(186,132)};
            // Рисуем замкнутую закрашенную кривую
            gr.FillClosedCurve(Brushes.LightBlue, Brow);
            // Обводка
            gr.DrawCurve(p, Brow);
        }
        void Ears_Paint()
        {
            // Рисуем закрашенный эллипс
            gr.FillPie(Brushes.LightGray, 115, 239, 50, 50, -80, -220);
            // Обводим
            gr.DrawArc(p, 115, 239, 50, 50, -80, -220);
            // Аналогичная операция для правого уха
            gr.FillPie(Brushes.LightGray, 312, 240, 40, 40, -87, 181);
            gr.DrawArc(p, 312, 240, 40, 40, -87, 181);
        }
        void Mouth_Paint()
        {
            // Массив точек для рта
            Point[] mouth = { new Point(309, 297), new Point(257, 293), new Point(195, 305) };
            // Обводка
            gr.DrawCurve(p, mouth);
            // Массив точек для 1 складки
            Point[] fold_one = { new Point(309, 285), new Point(321, 296), new Point(315, 310), new Point(305, 312) };
            // Обводка
            gr.DrawCurve(p, fold_one);
            // Массив точек для 2 складки
            Point[] fold_two = { new Point(188, 291), new Point(180, 304), new Point(188, 312), new Point(204, 315) };
            // Обводка
            gr.DrawCurve(p, fold_two);
        }
        void Mouth_Paint2()
        {
            //Массив точек для рта
            Point[] mouth = { new Point(271,282),new Point(293,280),new Point(311,278),new Point(323,289),new Point(323,303),new Point(317,313),
                new Point(297,310),
            new Point(257,318),new Point(237,316),new Point(223,311),new Point(215,299),new Point(213,290),new Point(223,276),new Point(237,274),
            new Point(255,278),new Point(271,282)};
            //Обводка
            gr.FillClosedCurve(Brushes.Black, mouth);

            Point[] Teeth5 = { new Point(245,302), new Point(256,307),new Point(256,316),
                new Point(243,317),new Point(231,314),new Point(234,306)};
            gr.FillClosedCurve(Brushes.White, Teeth5);
            gr.DrawClosedCurve(p, Teeth5);

            Point[] Tongue = { new Point(227,294), new Point(245,300), new Point(252,308), new Point(265,324), new Point(283,336),
            new Point(295,338),new Point(312,333),new Point(320,321),new Point(319,314),
                new Point(309,305),new Point(297,296),new Point(272,282),new Point(246,284)};
            gr.FillClosedCurve(Brushes.Red, Tongue);
            gr.DrawClosedCurve(p, Tongue);

            Point[] Tongue_h = { new Point(268, 292), new Point(281, 301), new Point(293, 314) };
            gr.DrawCurve(p, Tongue_h);

            Point[] Teeth1 = { new Point(223, 278), new Point(226, 292), new Point(237, 292), new Point(242, 286),
                new Point(243, 276), new Point(231, 274), new Point(223, 278) };
            gr.FillClosedCurve(Brushes.White, Teeth1);
            gr.DrawClosedCurve(p, Teeth1);

            Point[] Teeth2 = {new Point(249,277),new Point(259,280),new Point(269,282),new Point(268,292),new Point(255,294),
            new Point(249,285),new Point(248,284)};
            gr.FillClosedCurve(Brushes.White, Teeth2);
            gr.DrawClosedCurve(p, Teeth2);

            Point[] Teeth3 = {new Point(275,282), new Point(277,290) , new Point(287,296) ,
                new Point(295,291) , new Point(295,282) , new Point(286,281) };
            gr.FillClosedCurve(Brushes.White, Teeth3);
            gr.DrawClosedCurve(p, Teeth3);

            Point[] Teeth4 = { new Point(301,282), new Point(304,290), new Point(314,294),
                new Point(320,290),new Point(319,284), new Point(311,279)};
            gr.FillClosedCurve(Brushes.White, Teeth4);
            gr.DrawClosedCurve(p, Teeth4);

            Point[] Teeth6 = { new Point(219, 303), new Point(228, 302), new Point(231, 306), new Point(230, 312), new Point(222, 309) };
            gr.FillClosedCurve(Brushes.White, Teeth6);
            gr.DrawClosedCurve(p, Teeth6);

            Point[] m = { new Point(207, 306), new Point(217, 324), new Point(235, 328) };
            gr.DrawCurve(p, m);
        }
        void Hair_Paint()
        {
            // Массив точек для волос
            Point[] hair = {  new Point(215,0),new Point(251,44),new Point(303,0),new Point(328,0),new Point(320,73),new Point(395,66),
                new Point(348,135),new Point(401,168),new Point(349,202),new Point(389,248),new Point(337,264),
                new Point(361,300),new Point(335,300),new Point(345,323),new Point(127,334),
                new Point(135,306) , new Point(84,304) , new Point(100,273), new Point(43,250),
                new Point(101,208), new Point(28,172), new Point(105,138), new Point(65,55), new Point(159,62), new Point(162,0) ,new Point(215,0)};
            // Рисуем закрашенную ломаную
            gr.FillPolygon(Brushes.LightBlue, hair);
            // Обводка
            gr.DrawLines(p, hair);
        }
        void Neck_Paint()
        {
            // Массив точек для шеи
            Point[] neck = {new Point(202,365),new Point(201,365),new Point(200,367), new Point(197,376) , new Point(194,391) , new Point(209,397),
            new Point(229,398),new Point(243,395),new Point(257,388),new Point(258,380),new Point(258,374),new Point(258,373),new Point(257,373)};
            // Рисуем закрашенную кривую
            gr.FillClosedCurve(Brushes.LightGray, neck);
            // Обводка
            gr.DrawCurve(p, neck);
        }
        void T_shirt_Paint()
        {
            // Массив точек для футболки
            Point[] tshirt = { new Point(194,390),new Point(193, 390),new Point(193,391), new Point(196, 418), new Point(197,440),
                new Point(197,441),new Point(197, 442),
                new Point(198,442),new Point(262,442),new Point(263, 442),new Point(263,441),new Point(263,440),
                new Point(261, 417),new Point(258,389), new Point(258, 388),new Point(257,388) };
            // Рисуем закрашенную кривую
            gr.FillClosedCurve(Brushes.Turquoise, tshirt);
            // Обводим
            gr.DrawCurve(p, tshirt);
        }
        void Robe_Paint()
        {
            Point[] robe = { new Point(192, 387), new Point(101, 415), new Point(88, 443), new Point(323, 443), new Point(314, 415), new Point(258, 388) };
            gr.FillPolygon(Brushes.White, robe);
            gr.DrawLines(p, robe);
            gr.DrawLine(p, new Point(187, 406), new Point(168, 443));
            gr.DrawLine(p, new Point(270, 404), new Point(283, 443));
        }
    }
}
