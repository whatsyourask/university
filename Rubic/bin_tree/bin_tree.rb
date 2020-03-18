# Class node for binary tree
class Node
  # Create getter and setter for left, right, data
  attr_accessor :left, :right, :data
  # Constructor for class
  def initialize(data = nil)
    @left = nil
    @right = nil
    @data = data
  end
end

# Class binary tree
class BinTree
  # Create getter and setter for main_root
  attr_accessor :main_root
  @main_root = nil
  # Method for add a new node
  def add(data)
    if @main_root.nil?
      @main_root = Node.new(data)
    else
      current = @main_root
      loop do
        if data < current.data
          if current.left.nil?
            current.left = Node.new(data)
            break
          else
            current = current.left
            end
        elsif current.right.nil?
          current.right = Node.new(data)
          break
        else
          current = current.right
        end
      end
    end
  end
  # Overload of method 'to_s'
  def to_s
    to_s_r(@main_root)
  end
  # Recursive method for overload 'to_s'
  def to_s_r(root)
    unless root.nil?
      "#{to_s_r(root.left)}#{root.data} #{to_s_r(root.right)}"
    end
  end
  # Method for writing tree
  def write
    array = gets.split(' ').map{ |elem| elem.to_i }
    for i in array do
      add(i)
    end
  end
  # Method to remove node
  def delete(data)
    delete_r(@main_root, data)
  end
  # Recursive method to remove node(not working yet)
  def delete_r(root, data)
    if root.nil?
      return
    elsif root.data > data
      delete_r(root.left, data)
    elsif root.data < data
      delete_r(root.right, data)
    else
      current = root
      if root.left.nil?
        root = root.right
      elsif root.right.nil?
        root = root.left
      else
        p = root.right
        if p.left.nil?
          p.left = current.left
          root = p
        else
          q = p.left
          until q.left.nil? do
            q = q.left
            p = p.left
          end
          root.data = q.data
          p.left = q.right
        end
      end
    end
  end
  # Method to find the desired node
  def search(data)
    current = @main_root
    until current.nil? do
      if data == current.data
        return current
      elsif data < current.data
        current = current.left
      else
        current = current.right
      end
    end
    raise 1
  end
end