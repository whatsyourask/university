require 'Matrix'

class Graph
  attr_reader :m, :matrix

  def initialize(m = nil)
    if m.nil?
      puts "Write a count of vertex: "
      m = gets.to_i
    end
    create_matrix(m)
  end

  def create_matrix(m)
    @m = m
    @matrix = Matrix.scalar(@m, 0)
  end

  def write_matrix
    for i in 0...@m do
      puts "write vertices that have a path from #{i + 1} vertex	"
      for j in 0...@m do
        @matrix[i, j] = gets.chomp.to_i
      end
    end
  end

  def print_matrix
    puts @matrix
  end

  def test
    @matrix = Matrix[[0,7,9,0,0,14],
    [0,0,10,15,0,0],
    [0,10,0,11,0,2],
    [0,0,0,0,6,0],
    [0,0,0,0,0,0],
    [0,0,2,0,9,0]]
  end

  def search_way(v1, v2)
    processed, ways, prevs, processing = [],[],[],[]
    (0...@m).map do
      processed.push(0)
      ways.push(0)
      prevs.push(v1 - 1)
    end
    processing.push(v1 - 1)
    until processing.empty?
      min = 2**30 - 1
      node = processing.shift
      (0...@m).map do |i|
        elem = @matrix[node, i]
        unless elem.zero?
          processed[i] = 1 if processed[i].zero?
          if elem + ways[node] < ways[i] || ways[i].zero?
            ways[i] = elem + ways[node]
            prevs[i] = node
          end
        end
      end
      processed[node] = 2
      check = 0
      processed.each { |elem| check = 1 if elem != 2 }
      unless check.zero?
        (0...@m).map do |i|
          if ways[i] != 0 && ways[i] < min && processed[i] == 1
            min = ways[i]
            ind = i
            processing.push(ind)
          end
        end
      end
    end
    need = v2 - 1
    result = []
    puts "way = " + ways[v2 - 1].to_s
    str = "way:" + v2.to_s
    while need != v1 - 1
      need = prevs[need]
      result.push(need)
      str += "<-" + (need + 1).to_s
    end
    puts str
  end
end
