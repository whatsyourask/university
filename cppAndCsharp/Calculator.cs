using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace calculator
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        // Создаём матрицы
        int[,] A = new int[100, 100];
        int[,] B = new int[100, 100];
        int[,] C = new int[100, 100];
        // Создаем генератор случайный чисел(ДО 9)
        Random generator = new Random(9);
        // Кнопка умножения
        private void GenerateMatrix(int N)
        {
            dataGridView1.Rows.Clear();
            dataGridView1.Columns.Clear();
            dataGridView2.Rows.Clear();
            dataGridView2.Columns.Clear();
            dataGridView3.Rows.Clear();
            dataGridView3.Columns.Clear();
            // Создаём столбцы
            for (int i = 0; i < N; i++)
                dataGridView1.Columns.Add("", "");
            // Создаём строки,на 1 меньше при N-1
            for (int i = 0; i < N - 1; i++)
                dataGridView1.Rows.Add();
            for (int i = 0; i < N; i++)
                dataGridView2.Columns.Add("", "");
            for (int i = 0; i < N - 1; i++)
                dataGridView2.Rows.Add();
            for (int i = 0; i < N; i++)
                dataGridView3.Columns.Add("", "");
            for (int i = 0; i < N - 1; i++)
                dataGridView3.Rows.Add();
            // Генерируем матрицы A и B
            for (int i = 0; i < N; i++)
                for (int j = 0; j < N; j++)
                {
                    C[i, j] = 0;
                    A[i, j] = generator.Next(9);
                    dataGridView1.Rows[i].Cells[j].Value = Convert.ToString(A[i, j]);
                    B[i, j] = generator.Next(9);
                    dataGridView2.Rows[i].Cells[j].Value = Convert.ToString(B[i, j]);
                }
        }
        private void button1_Click(object sender, EventArgs e)
        {
            // Берём из TextBox ранг матрицы
            int N = Convert.ToInt32(textBox1.Text);
            GenerateMatrix(N);
            // Перемножаем матрицы A и B
            for (int i = 0; i < N; i++)
                for (int j = 0; j < N; j++)
                    for (int q = 0; q < N; q++)
                    {
                        C[i, j] += A[i, q] * B[q, j];
                        dataGridView3.Rows[i].Cells[j].Value = Convert.ToString(C[i, j]);
                    }
            
        }
        // Кнопка сложения
        private void button2_Click(object sender, EventArgs e)
        {
            // Берём из TextBox ранг матрицы
            int N = Convert.ToInt32(textBox1.Text);
            GenerateMatrix(N);
            for (int i = 0; i < N; i++)
                for (int j = 0; j < N; j++)
                {
                    C[i, j] = A[i, j] + B[i, j];
                    dataGridView3.Rows[i].Cells[j].Value = Convert.ToString(C[i, j]);
                }
        }
    }
}
