def scale(num,sys)
  ch_sys = ['0']
  if sys >= 10
    a = sys - (sys / 10 - 1) * 10 - sys % 10
    for i in 1...a do
      ch_sys.push((ch_sys[i - 1].ord + 1).chr)
    end
    ch_sys[10] = 'A'
    for i in 11...sys do
      ch_sys.push((ch_sys[i-1].ord + 1).chr)
    end
  else
    for i in 1...sys do
      ch_sys.push((ch_sys[i-1].ord + 1).chr)
    end
  end
  new_num = []
  while num > 0
    new_num.push(ch_sys[num % sys])
    num /= sys
  end
  new_num.reverse!
  puts new_num.join
end