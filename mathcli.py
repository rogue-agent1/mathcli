#!/usr/bin/env python3
"""mathcli - Command-line calculator and math utility."""
import argparse, math, sys, statistics, operator, re

SAFE_FUNCS = {
    'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'log': math.log, 'log2': math.log2, 'log10': math.log10,
    'exp': math.exp, 'abs': abs, 'ceil': math.ceil, 'floor': math.floor,
    'pow': pow, 'round': round, 'min': min, 'max': max,
    'pi': math.pi, 'e': math.e, 'tau': math.tau, 'inf': float('inf'),
    'factorial': math.factorial, 'gcd': math.gcd,
    'radians': math.radians, 'degrees': math.degrees,
    'hypot': math.hypot, 'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
}

def safe_eval(expr):
    return eval(expr, {"__builtins__": {}}, SAFE_FUNCS)

def main():
    p = argparse.ArgumentParser(description='CLI calculator')
    sub = p.add_subparsers(dest='cmd')
    
    calc = sub.add_parser('eval', help='Evaluate expression')
    calc.add_argument('expr', nargs='+')
    
    st = sub.add_parser('stats', help='Statistics on numbers')
    st.add_argument('numbers', nargs='*', type=float)
    st.add_argument('-f', '--file', help='Read from file')
    
    cv = sub.add_parser('base', help='Number base conversion')
    cv.add_argument('number')
    cv.add_argument('--from-base', type=int, default=10)
    
    pct = sub.add_parser('percent', help='Percentage calculations')
    pct.add_argument('a', type=float)
    pct.add_argument('op', choices=['of','change','is'])
    pct.add_argument('b', type=float)
    
    fib = sub.add_parser('fib', help='Fibonacci')
    fib.add_argument('n', type=int)
    
    prm = sub.add_parser('prime', help='Check if prime / list primes')
    prm.add_argument('n', type=int)
    prm.add_argument('--list', action='store_true', help='List primes up to N')
    
    args = p.parse_args()
    if not args.cmd: p.print_help(); return
    
    if args.cmd == 'eval':
        expr = ' '.join(args.expr)
        try:
            result = safe_eval(expr)
            print(result)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr); sys.exit(1)
    
    elif args.cmd == 'stats':
        nums = list(args.numbers)
        if args.file:
            with open(args.file) as f:
                nums.extend(float(line.strip()) for line in f if line.strip())
        if not nums:
            nums = [float(line.strip()) for line in sys.stdin if line.strip()]
        print(f"Count:    {len(nums)}")
        print(f"Sum:      {sum(nums):.6g}")
        print(f"Mean:     {statistics.mean(nums):.6g}")
        print(f"Median:   {statistics.median(nums):.6g}")
        if len(nums) > 1:
            print(f"Stdev:    {statistics.stdev(nums):.6g}")
            print(f"Variance: {statistics.variance(nums):.6g}")
        print(f"Min:      {min(nums):.6g}")
        print(f"Max:      {max(nums):.6g}")
        print(f"Range:    {max(nums)-min(nums):.6g}")
    
    elif args.cmd == 'base':
        n = int(args.number, args.from_base)
        print(f"Dec: {n}\nHex: {hex(n)}\nOct: {oct(n)}\nBin: {bin(n)}")
    
    elif args.cmd == 'percent':
        if args.op == 'of': print(f"{args.a}% of {args.b} = {args.a/100*args.b:.6g}")
        elif args.op == 'change': print(f"Change: {(args.b-args.a)/args.a*100:.2f}%")
        elif args.op == 'is': print(f"{args.a} is {args.a/args.b*100:.2f}% of {args.b}")
    
    elif args.cmd == 'fib':
        a, b = 0, 1
        for i in range(args.n):
            print(a, end=' ')
            a, b = b, a + b
        print()
    
    elif args.cmd == 'prime':
        if args.list:
            sieve = [True] * (args.n + 1)
            sieve[0] = sieve[1] = False
            for i in range(2, int(args.n**0.5) + 1):
                if sieve[i]:
                    for j in range(i*i, args.n+1, i): sieve[j] = False
            primes = [i for i, v in enumerate(sieve) if v]
            print(f"{len(primes)} primes up to {args.n}: {' '.join(map(str, primes[:50]))}" + ("..." if len(primes) > 50 else ""))
        else:
            if args.n < 2: print(f"{args.n} is not prime"); return
            for i in range(2, int(args.n**0.5) + 1):
                if args.n % i == 0:
                    factors = []
                    n = args.n
                    d = 2
                    while d * d <= n:
                        while n % d == 0: factors.append(d); n //= d
                        d += 1
                    if n > 1: factors.append(n)
                    print(f"{args.n} is NOT prime ({' × '.join(map(str, factors))})")
                    return
            print(f"{args.n} IS prime")

if __name__ == '__main__':
    main()
