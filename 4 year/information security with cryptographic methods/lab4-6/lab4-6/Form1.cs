using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Numerics;

namespace lab4_6
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                BigInteger a = Convert.ToInt64(textBox1.Text);
                BigInteger b = Convert.ToInt64(textBox2.Text);
                BigInteger p = Convert.ToInt64(textBox3.Text);
                BigInteger x = GelfondShanksAlgorithm(a, b, p);
                textBox4.Text = Convert.ToString(x);
            }
            catch (Exception ex)
            {
                ErrorHandler(ex);
            }
        }
        // https://ilovecalc.com/calcs/maths/baby-step-giant-step/1382/
        private BigInteger GelfondShanksAlgorithm(BigInteger a, BigInteger b, BigInteger p)
        {
            a %= p;
            b %= p;
            if (b == 1)
                return 0;
            if (a == b)
                return 1;
            BigInteger m = (BigInteger)Math.Sqrt((double)p) + BigInteger.One;
            BigInteger k = m;
            BigInteger temp = BigInteger.Multiply(m, k);
            Debug.Assert(temp > p, "m * k > p");
            List<BigInteger> bigSteps = findBigSteps(a, m, k, p);
            /*bigSteps.ForEach(x => Console.WriteLine("Elem: " + x));*/
            BigInteger smallSteps = findSmallSteps(bigSteps, a, b, m, p);
            return smallSteps;
        }
        private void ErrorHandler(Exception ex)
        {
            MessageBox.Show(ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
        private List<BigInteger> findBigSteps(BigInteger a, BigInteger m, BigInteger k, BigInteger p)
        {
            List<BigInteger> temp = new List<BigInteger>();
            for (int i = 1; i <= k; i++)
            {
                BigInteger element = BigInteger.ModPow(a, i * m, p);
                temp.Add(element);
            }
            return temp;
        }
        private BigInteger findSmallSteps(List<BigInteger> bigSteps, BigInteger a, BigInteger b, BigInteger m, BigInteger p)
        {
            Console.WriteLine("Shanks iterations: " + m);
            for (int i = 1; i <= m; i++)
            {
                if (i % 1000 == 0)
                    Console.WriteLine("inside i - " + i);
                BigInteger newSmallElem = b * BigInteger.Pow(a, i) % p;
                BigInteger bigStepsIndex = -1;
                try
                {
                    bigStepsIndex = bigSteps.IndexOf(newSmallElem);
                }
                catch { }
                if (bigStepsIndex != -1)
                {
                    BigInteger temp = bigStepsIndex + 1;
                    return temp * m - i;
                }
            }
            return BigInteger.Zero;
        }

        private void button2_Click(object sender, EventArgs e)
        {
            /*try
            {
                BigInteger p = Convert.ToInt64(textBox5.Text);
                BigInteger a = Convert.ToInt64(textBox6.Text);
                BigInteger b = Convert.ToInt64(textBox7.Text);
                BigInteger x = PollardsRhoAlgorithmForLogarithms(p, a, b);
                textBox8.Text = Convert.ToString(x);

            } catch (Exception ex)
            {
                ErrorHandler(ex);
            }*/
            try
            {
                BigInteger a = Convert.ToInt64(textBox5.Text);
                BigInteger b = Convert.ToInt64(textBox6.Text);
                BigInteger p = Convert.ToInt64(textBox7.Text);
                BigInteger x = PollardsRhoAlgorithmForLogarithms(a, b, p);
                textBox8.Text = Convert.ToString(x);
            } catch (Exception ex)
            {
                ErrorHandler(ex);
            }
        }
        static int modInverse(BigInteger a, BigInteger m)
        {

            for (int x = 1; x < m; x++)
                if (((a % m) * (x % m)) % m == 1)
                    return x;
            return 1;
        }
        private BigInteger PollardsRhoAlgorithmForLogarithms(BigInteger g, BigInteger h, BigInteger p)
        {
            BigInteger q = (long)((p - 1) / 2);
            BigInteger x = g * h;
            BigInteger a = 1;
            BigInteger b = 1;
            BigInteger X = x;
            BigInteger A = a;
            BigInteger B = b;

            for (int i = 1; i < p; i++)
            {
                BigInteger[] temp = xab(x, a, b, new BigInteger[] { g, h, p, q });
                x = temp[0];
                a = temp[1];
                b = temp[2];
                temp = xab(X, A, B, new BigInteger[] {g, h, p, q});
                X = temp[0];
                A = temp[1];
                B = temp[2];
                temp = xab(X, A, B, new BigInteger[] {g, h, p, q});
                X = temp[0];
                A = temp[1];
                B = temp[2];
                if (x == X)
                    break;
            }
            BigInteger nom = a - A;
            BigInteger denom = B - b;
            BigInteger rev = (modInverse(denom, q) * nom) % q;
            if (verify(g, h, p, rev))
                return rev;
            return rev + q;
        }
        private BigInteger[] xab(BigInteger x, BigInteger a, BigInteger b, BigInteger[] arr)
        {
            BigInteger sub = x % 3;
            BigInteger g = arr[0], h = arr[1], p = arr[2], q = arr[3];
            if (sub == 0)
            {
                x = x * g % p;
                a = (a + 1) % q;
            }
            if (sub == 1)
            {
                x = x * h % p;
                b = (b + 1) % q;
            }
            if (sub == 2)
            {
                x = x * x % p;
                a = a * 2 % q;
                b = b * 2 % q;
            }
            return new BigInteger[] {x, a, b};
        }
        private bool verify(BigInteger g, BigInteger h, BigInteger p, BigInteger rev)
        {
            return BigInteger.ModPow(g, rev, p) == h;
        }
    }
}
