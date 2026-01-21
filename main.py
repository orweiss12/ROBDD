# main.py
from robdd import ROBDD

def formula_a(vals):
    """Assignment 3, Q1a: (a and !c) or (b xor d)"""
    return (vals['a'] and (not vals['c'])) or (vals['b'] != vals['d'])

def formula_b(vals):
    """Assignment 3, Q1b: Majority function (at least 3 ones)"""
    vars_list = ['x1', 'x2', 'x3', 'x4', 'x5']
    return sum(1 for v in vars_list if vals[v]) >= 3

def formula_c(vals):
    """Assignment 3, Q1c: Comparison X > Y (Interleaved ordering)"""
    # x3 is MSB (Most Significant Bit)
    val_x = (int(vals['x3']) * 4) + (int(vals['x2']) * 2) + int(vals['x1'])
    val_y = (int(vals['y3']) * 4) + (int(vals['y2']) * 2) + int(vals['y1'])
    return val_x > val_y

def formula_custom(vals):
    """Custom Formula: Logical Implication (P -> Q)"""
    return (not vals['P']) or vals['Q']

if __name__ == "__main__":
    print("--- Generating ROBDDs for Assignment 3 ---")

    # 1. Formula A
    print("Building Formula A...")
    bdd_a = ROBDD(['a', 'b', 'c', 'd'])
    bdd_a.visualize(bdd_a.build(formula_a), "output_formula_a")

    # 2. Formula B
    print("Building Formula B...")
    bdd_b = ROBDD(['x1', 'x2', 'x3', 'x4', 'x5'])
    bdd_b.visualize(bdd_b.build(formula_b), "output_formula_b")

    # 3. Formula C (With optimized interleaved ordering)
    print("Building Formula C...")
    # Note: Ordering is x3, y3... to create an efficient structure
    bdd_c = ROBDD(['x3', 'y3', 'x2', 'y2', 'x1', 'y1'])
    bdd_c.visualize(bdd_c.build(formula_c), "output_formula_c")

    # 4. Custom Formula
    print("Building Custom Formula...")
    bdd_d = ROBDD(['P', 'Q'])
    bdd_d.visualize(bdd_d.build(formula_custom), "output_custom_example")
    
    print("\nDone! Images saved in the current directory.")
