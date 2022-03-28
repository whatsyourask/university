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
            BigInteger p = Convert.ToInt64(textBox5.Text);
                BigInteger a = Convert.ToInt64(textBox6.Text);
                BigInteger b = Convert.ToInt64(textBox7.Text);
                BigInteger x = PollardsRhoAlgorithmForLogarithms(p, a, b);
                textBox8.Text = Convert.ToString(x);
        }
        static int modInverse(BigInteger a, BigInteger m)
        {

            for (int x = 1; x < m; x++)
                if (((a % m) * (x % m)) % m == 1)
                    return x;
            return 1;
        }
        private BigInteger PollardsRhoAlgorithmForLogarithms(BigInteger p, BigInteger a, BigInteger b)
        {
            a %= p;
            b %= p;
            BigInteger n = p - 1;
            List<BigInteger> h_seq = new List<BigInteger>();
            List<BigInteger> x_seq = new List<BigInteger>();
            List<BigInteger> y_seq = new List<BigInteger>();
            BigInteger x_i = 0, y_i = 0, h_i = 1;
            int i = 0;
            Dictionary<BigInteger, BigInteger> s_table = new Dictionary<BigInteger, BigInteger>();
            while (true)
            {
                h_seq.Add(h_i);
                x_seq.Add(x_i);
                y_seq.Add(y_i);
                i += 1;
                if (0 <= h_i && h_i < (long)(p / 3)) // G1
                {
                    h_i = (b * h_i) % p;
                    y_i = (y_i + 1) % n;
                } else if ((long)(p / 3) <= h_i && (h_i < 2 * (long)(p / 3))) // G2
                {
                    h_i = (h_i * h_i) % p;
                    x_i = (x_i * 2) % n;
                    y_i = (y_i * 2) % n;
                } else
                {
                    h_i = (a * h_i) % p;
                    x_i = (x_i + 1) % n;
                }
                BigInteger tmp = i - 1, m = 0;
                while (tmp != 0 && tmp % 2 != 0)
                {
                    tmp = (long)(tmp / 2);
                    m += 1;
                }
                s_table[m] = i - 1;
                BigInteger t = -1;
                foreach(var item in s_table)
                {
                    if (h_seq[(int)item.Value] == h_i)
                        t = item.Value;
                }
                if (t != -1)
                {
                    BigInteger x_diff = (x_i - x_seq[(int)t]) % n;
                    BigInteger y_diff = (y_i - y_seq[(int)t]) % n;
                    if (x_diff == 0 && y_diff == 0) {
                        return 0;
                    }
                    if (BigInteger.GreatestCommonDivisor(y_diff, n) == 1)
                    {
                        return (-x_diff * modInverse(y_diff, n)) % n;
                    }
                    BigInteger d = BigInteger.GreatestCommonDivisor(y_diff, n);
                    BigInteger n_0 = (long)(n / d);
                    BigInteger log_0 = (-x_diff * modInverse(y_diff, n)) % n_0;
                    for (int j = 0; j < d; j++)
                    {
                        BigInteger log = log_0 + j * n_0;
                        if (BigInteger.ModPow(a, log, p) == (b % p))
                        {
                            return log % n;
                        }
                    }
                }
            }
        }
    }
}
