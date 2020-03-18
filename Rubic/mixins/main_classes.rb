class Point
  # Automatic creates getters and setters
  attr_accessor :x, :y
  # Constructor
  def initialize(x, y)
      @x = x
      @y = y
  end
  # Method for printing coordinates
  def print
    puts "(#{x},#{y})"
  end
  # Method for calculating distance
  def distance(oth_p)
    Math.sqrt((x - oth_p.x)**2 + (y - oth_p.y)**2)
  end
end

class Triangle
  # Automatic creates getters
  attr_reader :p1, :p2, :p3
  # Constructor
  def initialize(*args)
    # Here,the constructor takes an array "args" and I control the number of elements in this array.
    if args.size == 6
      @p1 = Point.new(args[0], args[1])
      @p2 = Point.new(args[2], args[3])
      @p3 = Point.new(args[4], args[5])
    elsif args.size == 3
      @p1 = args[0]
      @p2 = args[1]
      @p3 = args[2]
    else
      raise "Wrong number of arguments"
    end
  end
  # Method for printing points of triangle...
  def print
    @p1.print
    @p2.print
    @p3.print
  end
  # Method for calculating perimeter...
  def perimeter
    @p1.distance(@p2) + @p2.distance(@p3) + @p3.distance(@p1)
  end
  # Method for calculating square...
  def square
    p = perimeter / 2
    Math.sqrt(p * (p - @p1.distance(@p2)) * (p - @p2.distance(@p3)) * (p - @p3.distance(@p1)))
  end
  # Method for checking:a point inside or outside?
  def in_figure(p)
    s = square
    s1 = Triangle.new(@p1, @p2, p).square
    s2 = Triangle.new(@p2, @p3, p).square
    s3 = Triangle.new(@p1, @p3, p).square
    ((s1 + s2 + s3 - s).abs <= 0.0001) ? true : false
  end
end

class Tetragon < Triangle # inherited from the class triangle
  attr_reader :p4
  def initialize(*args)
    if args.size == 8
      # Call the superclass constructor
      super(args[0], args[1], args[2], args[3], args[4], args[5])
      @p4 = Point.new(args[6], args[7])
    elsif args.size == 4
      super(args[0], args[1], args[2])
      @p4 = args[3]
    else
      raise "Wrong number of arguments"
    end
  end

  def print
    # Call the superclass method with the same name
    super
    @p4.print
  end

  def perimeter
    @p1.distance(@p2) + @p2.distance(@p3) + @p3.distance(@p4) + @p4.distance(@p1)
  end

  def in_figure(p)
    Triangle.new(@p1, @p2, @p3).in_figure(p) ||
      Triangle.new(@p1, @p2, @p4).in_figure(p) ||
      Triangle.new(@p1, @p3, @p4).in_figure(p) ||
      Triangle.new(@p2, @p3, @p4).in_figure(p)
  end
  # Method for checking:is tetragon convex or not?
  def is_convex
    !Triangle.new(@p1, @p2, @p3).in_figure(@p4) &&
      !Triangle.new(@p1, @p2, @p4).in_figure(@p3) &&
      !Triangle.new(@p1, @p4, @p3).in_figure(@p2) &&
      !Triangle.new(@p4, @p2, @p3).in_figure(@p1)
  end

  def square
    p = perimeter / 2
    Math.sqrt((p - @p1.distance(@p2)) * (p - @p2.distance(@p3)) * (p - @p3.distance(@p4))*(p - @p4.distance(@p1)))
  end
end