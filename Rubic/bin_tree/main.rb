load 'bin_tree.rb'

tree = BinTree.new
tree.write
puts tree
tree.add(44)
puts tree
puts tree.search(44)
tree.delete(5)
puts tree
