using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Картинка
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            Paint += Hair_Paint;
            Paint += Robe_Paint;
            Paint += T_shirt_Paint;
            Paint += Neck_Paint;
            Paint += Head_Paint;
            Paint += Eyes_Paint;
            Paint += Nose_Paint;
            Paint += Brow_Paint;
            Paint += Ears_Paint;
            Paint += Mouth_Paint;
        }
        static float width = 2.5f;
        static Pen p = new Pen(Color.Black, width);
        private void Head_Paint(object sender, PaintEventArgs e)
        {
            // Массив точек для головы
            Point[] head = { new Point(240, 72), new Point(210, 75), new Point(180, 90), new Point(147, 130), new Point(133, 228),
                new Point(160, 333), new Point(240, 374), new Point(317, 329), new Point(332, 220),
                new Point(322, 132), new Point(300, 95), new Point(272, 76),new Point(240, 72) };
            // Рисуем замкнутую закрашенную кривую
            e.Graphics.FillClosedCurve(Brushes.LightGray, head);
            // Обводка
            e.Graphics.DrawCurve(p, head);
        }
        private void Eyes_Paint(object sender, PaintEventArgs e)
        {
            // Массив точек для 1 глаза
            Point[] eye_one = { new Point(185, 157),new Point(173,167),new Point(165, 190), new Point(182, 220), new Point(222, 225),
                new Point(244,209),new Point(248, 185),new Point(245, 170),new Point(232, 158)};
            // Рисуем незамкнутую закрашенную кривую
            e.Graphics.FillClosedCurve(Brushes.LightGray, eye_one);
            // Обводка
            e.Graphics.DrawCurve(p, eye_one);

            int x = 95; // смещение глаза вправо
            // Массив точек для 2 глаза
            Point[] eye_two = { new Point(185+x, 157),new Point(173+x,167),new Point(165+x, 185), new Point(182+x, 220), new Point(222+x, 225),
                new Point(244+x,209),new Point(248+x, 185),new Point(245+x, 170),new Point(229+x, 155)};
            // Рисуем незамкнутую закрашенную кривую
            e.Graphics.FillClosedCurve(Brushes.LightGray, eye_two);
            // Обводка
            e.Graphics.DrawCurve(p, eye_two);

            // Массив точек для 1 глаза(Заполнение белым)
            Point[] white_eye_one = {new Point(165+46,185),new Point(165+45,185),new Point(165+40,186),new Point(165, 188), new Point(182, 220), new Point(222, 225),
                new Point(244,209),new Point(248,186),new Point(248, 185),new Point(245, 185),new Point(165+46,185)};
            // Рисуем незамкнутую закрашенную кривую
            e.Graphics.FillClosedCurve(Brushes.White, white_eye_one);
            // Обводка
            e.Graphics.DrawClosedCurve(p, white_eye_one);

            // Массив точек для 2 глаза(Заполнение белым)
            Point[] white_eye_two = {new Point(165+46+x,185),new Point(165+45+x,185),new Point(165+40+x,186),new Point(165+x, 188), new Point(182+x, 220), new Point(222+x, 225),
                new Point(244+x,209),new Point(248+x,186),new Point(248+x, 185),new Point(245+x, 185),new Point(165+46+x,185)};
            // Рисуем незамкнутую закрашенную кривую
            e.Graphics.FillClosedCurve(Brushes.White, white_eye_two);
            // Обводка
            e.Graphics.DrawClosedCurve(p, white_eye_two);

            // Рисуем зрачки
            e.Graphics.FillEllipse(Brushes.Black, 220, 183, 13, 13);
            e.Graphics.FillEllipse(Brushes.Black, 220 + x, 183, 13, 13);

            // Массив точек для левого мешка под глазом
            Point[] bag_left = { new Point(166, 229), new Point(174,237),new Point(190, 243), new Point(216, 240) };
            // Рисуем кривую линию
            e.Graphics.DrawCurve(p, bag_left);

            // Массив точек для правого мешка под глазом
            Point[] bag_right = { new Point(288, 239),new Point(304,241), new Point(318, 239),new Point(331,229), new Point(334, 220) };
            // Рисуем незамкнутую закрашенную кривую
            e.Graphics.FillClosedCurve(Brushes.LightGray, bag_right);
            // Рисуем обводку кривой
            e.Graphics.DrawCurve(p, bag_right);

        }
        private void Nose_Paint(object sender, PaintEventArgs e)
        {
            // Массив точек для носа
            Point[] nose_points = { new Point(249, 238), new Point(257, 255), new Point(271, 268),new Point(277,253), new Point(277, 241), new Point(272, 221) };
            // Рисуем кривую
            e.Graphics.DrawCurve(p, nose_points);
        }
        private void Brow_Paint(object sender, PaintEventArgs e)
        {
            // Массив точек для брови
            Point[] Brow = { new Point(186,132),new Point(183,136),new Point(184, 142), new Point(190, 143) , new Point(221, 129) , new Point(259, 121) , new Point(298, 129) , new Point(319, 138),
            new Point(325, 136),new Point(319, 124),new Point(295, 111),new Point(259, 106),new Point(221, 112),new Point(190, 127),new Point(186,132)};
            // Рисуем замкнутую закрашенную кривую
            e.Graphics.FillClosedCurve(Brushes.LightBlue, Brow);
            // Обводка
            e.Graphics.DrawCurve(p, Brow);
        }
        private void Ears_Paint(object sender,PaintEventArgs e)
        {   
            // Рисуем закрашенный эллипс
            e.Graphics.FillPie(Brushes.LightGray, 115, 239, 50, 50,-80,-220);
            // Обводим
            e.Graphics.DrawArc(p, 115, 239, 50, 50, -80, -220);
            // Аналогичная операция для правого уха
            e.Graphics.FillPie(Brushes.LightGray, 312, 240, 40, 40, -87, 181);
            e.Graphics.DrawArc(p, 312, 240, 40, 40, -87, 181);
        }
        private void Mouth_Paint(object sender,PaintEventArgs e)
        {
            // Массив точек для рта
            Point[] mouth = { new Point(309, 297), new Point(257, 293), new Point(195, 305) };
            // Обводка
            e.Graphics.DrawCurve(p, mouth);
            // Массив точек для 1 складки
            Point[] fold_one = { new Point(309, 285), new Point(321, 296), new Point(315, 310), new Point(305, 312) };
            // Обводка
            e.Graphics.DrawCurve(p, fold_one);
            // Массив точек для 2 складки
            Point[] fold_two = { new Point(188, 291), new Point(180, 304), new Point(188, 312), new Point(204, 315) };
            // Обводка
            e.Graphics.DrawCurve(p, fold_two);
        }
        private void Mouth_Paint2(object sender, PaintEventArgs e)
        {
            //Массив точек для рта
            Point[] mouth = { new Point(271,282),new Point(293,280),new Point(311,278),new Point(323,289),new Point(323,303),new Point(317,313),
                new Point(297,310),
            new Point(257,318),new Point(237,316),new Point(223,311),new Point(215,299),new Point(213,290),new Point(223,276),new Point(237,274),
            new Point(255,278),new Point(271,282)};
            //Обводка
            e.Graphics.FillClosedCurve(Brushes.Black, mouth);

            Point[] Teeth5 = { new Point(245,302), new Point(256,307),new Point(256,316),
                new Point(243,317),new Point(231,314),new Point(234,306)};
            e.Graphics.FillClosedCurve(Brushes.White, Teeth5);
            e.Graphics.DrawClosedCurve(p, Teeth5);

            Point[] Tongue = { new Point(227,294), new Point(245,300), new Point(252,308), new Point(265,324), new Point(283,336),
            new Point(295,338),new Point(312,333),new Point(320,321),new Point(319,314),
                new Point(309,305),new Point(297,296),new Point(272,282),new Point(246,284)};
            e.Graphics.FillClosedCurve(Brushes.Red, Tongue);
            e.Graphics.DrawClosedCurve(p, Tongue);

            Point[] Tongue_h = { new Point(268, 292), new Point(281, 301), new Point(293, 314) };
            e.Graphics.DrawCurve(p, Tongue_h);

            Point[] Teeth1 = { new Point(223, 278), new Point(226, 292), new Point(237, 292), new Point(242, 286),
                new Point(243, 276), new Point(231, 274), new Point(223, 278) };
            e.Graphics.FillClosedCurve(Brushes.White, Teeth1);
            e.Graphics.DrawClosedCurve(p, Teeth1);

            Point[] Teeth2 = {new Point(249,277),new Point(259,280),new Point(269,282),new Point(268,292),new Point(255,294),
            new Point(249,285),new Point(248,284)};
            e.Graphics.FillClosedCurve(Brushes.White, Teeth2);
            e.Graphics.DrawClosedCurve(p, Teeth2);

            Point[] Teeth3 = {new Point(275,282), new Point(277,290) , new Point(287,296) ,
                new Point(295,291) , new Point(295,282) , new Point(286,281) };
            e.Graphics.FillClosedCurve(Brushes.White, Teeth3);
            e.Graphics.DrawClosedCurve(p, Teeth3);

            Point[] Teeth4 = { new Point(301,282), new Point(304,290), new Point(314,294),
                new Point(320,290),new Point(319,284), new Point(311,279)};
            e.Graphics.FillClosedCurve(Brushes.White, Teeth4);
            e.Graphics.DrawClosedCurve(p, Teeth4);

            Point[] Teeth6 = { new Point(219, 303), new Point(228, 302), new Point(231, 306), new Point(230, 312), new Point(222, 309) };
            e.Graphics.FillClosedCurve(Brushes.White, Teeth6);
            e.Graphics.DrawClosedCurve(p, Teeth6);

            Point[] m = { new Point(207, 306), new Point(217, 324), new Point(235, 328) };
            e.Graphics.DrawCurve(p, m);
        }
        private void Hair_Paint(object sender,PaintEventArgs e)
        {
            // Массив точек для волос
            Point[] hair = {  new Point(215,0),new Point(251,44),new Point(303,0),new Point(328,0),new Point(320,73),new Point(395,66),
                new Point(348,135),new Point(401,168),new Point(349,202),new Point(389,248),new Point(337,264),
                new Point(361,300),new Point(335,300),new Point(345,323),new Point(127,334),
                new Point(135,306) , new Point(84,304) , new Point(100,273), new Point(43,250),
                new Point(101,208), new Point(28,172), new Point(105,138), new Point(65,55), new Point(159,62), new Point(162,0) ,new Point(215,0)};
            // Рисуем закрашенную ломаную
            e.Graphics.FillPolygon(Brushes.LightBlue, hair);
            // Обводка
            e.Graphics.DrawLines(p, hair);
        }
        private void Neck_Paint(object sender,PaintEventArgs e)
        {
            // Массив точек для шеи
            Point[] neck = {new Point(202,365),new Point(201,365),new Point(200,367), new Point(197,376) , new Point(194,391) , new Point(209,397),
            new Point(229,398),new Point(243,395),new Point(257,388),new Point(258,380),new Point(258,374),new Point(258,373),new Point(257,373)};
            // Рисуем закрашенную кривую
            e.Graphics.FillClosedCurve(Brushes.LightGray, neck);
            // Обводка
            e.Graphics.DrawCurve(p, neck);
        }
        private void T_shirt_Paint(object sender,PaintEventArgs e)
        {
            // Массив точек для футболки
            Point[] tshirt = { new Point(194,390),new Point(193, 390),new Point(193,391), new Point(196, 418), new Point(197,440),
                new Point(197,441),new Point(197, 442),
                new Point(198,442),new Point(262,442),new Point(263, 442),new Point(263,441),new Point(263,440),
                new Point(261, 417),new Point(258,389), new Point(258, 388),new Point(257,388) };
            // Рисуем закрашенную кривую
            e.Graphics.FillClosedCurve(Brushes.Turquoise, tshirt);
            // Обводим
            e.Graphics.DrawCurve(p, tshirt);
        }
        private void Robe_Paint(object sender,PaintEventArgs e)
        {
            Point[] robe = { new Point(192,387), new Point(101,415), new Point(88,443), new Point(323,443), new Point(314,415), new Point(258,388) };
            e.Graphics.FillPolygon(Brushes.White, robe);
            e.Graphics.DrawLines(p, robe);
            e.Graphics.DrawLine(p, new Point(187, 406), new Point(168, 443));
            e.Graphics.DrawLine(p, new Point(270, 404), new Point(283, 443));
        }
    }
}
