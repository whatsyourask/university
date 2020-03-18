def get_command
  command = gets.to_i
end

def get_value
  puts "write the value: "
  value = gets.to_i
end

def get_filename
  puts "write the file name: "
  filename = gets.chomp
end

def storage
  puts "=========Command List=========\n
  [ 1 ]:Show storage.\n
  [ 2 ]:Add to begin of storage.\n
  [ 3 ]:Add to end of storage.\n
  [ 4 ]:Delete by position.\n
  [ 5 ]:Write storage in file.\n
  [ 6 ]:Read storage from file.\n
  [ 7 ]:Sort storage.\n
  [ 0 ]:Exit.\n"
  v = []
  command = -1
  while command != 0
    command = get_command
    case command
    when 0 then
      puts "Exit...\n"
    when 1 then
      if v.empty?
        puts "Storage is empty.\n"
      else
        string = v.to_s
        puts "STORAGE: " + string
      end
    when 2 then
      value = get_value
      if v.empty?
        v.push(value)
      else
        v.insert(0, value)
      end
      puts "Added to begin of storage.\n"
    when 3 then
      value = get_value
      v.push(value)
      puts "Added to end of storage.\n"
    when 4 then
      puts "write the position: "
      position = gets.to_i
      v.delete_at(position-1)
      puts "Deleted by position from storage.\n"
    when 5 then
      filename = get_filename
      File.open(filename, 'w'){ |file| file.puts v.map{ |elem| elem.to_s}.join(' ') }
      puts "Wrote storage in file.\n"
    when 6 then
      filename = get_filename
      string = File.open(filename, 'r'){ |file| file.read }
      v = string.split(' ').map{ |elem| elem.to_i }
      puts "Read storage out file.\n"
    when 7 then
      v.sort
      puts "Storage sorted.\n"
    else
      puts "[ERROR]:INCORRECT VALUE!!!\n"
    end
  end
end