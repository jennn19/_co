import sys
import os

COMP_TABLE = {
    "0": "0101010",  "1": "0111111",  "-1": "0111010",
    "D": "0001100",  "A": "0110000",  "!D": "0001101",
    "!A": "0110001", "-D": "0001111", "-A": "0110011",
    "D+1": "0011111","A+1": "0110111","D-1": "0001110",
    "A-1": "0110010","D+A": "0000010","D-A": "0010011",
    "A-D": "0000111","D&A": "0000000","D|A": "0010101",
    "M": "1110000",  "!M": "1110001", "-M": "1110011",
    "M+1": "1110111","M-1": "1110010","D+M": "1000010",
    "D-M": "1010011","M-D": "1000111","D&M": "1000000",
    "D|M": "1010101"
}

DEST_TABLE = {
    "": "000",    "M": "001",   "D": "010",   "MD": "011",
    "A": "100",   "AM": "101",  "AD": "110",  "AMD": "111"
}

JUMP_TABLE = {
    "": "000",    "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}

def init_symbol_table():
    symbols = {
        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
        "SCREEN": 16384, "KBD": 24576
    }
    for i in range(16):
        symbols[f"R{i}"] = i
    return symbols

def clean_lines(raw_lines):
    cleaned = []
    for line in raw_lines:
        line = line.split("//")[0]
        line = "".join(line.split())
        if line:
            cleaned.append(line)
    return cleaned

def assemble(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = clean_lines(f.readlines())

    symbols = init_symbol_table()

    # 第一次掃描：記錄所有 (LABEL) 的 ROM 位址
    instructions = []
    rom_address = 0
    for line in lines:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            symbols[label] = rom_address
        else:
            instructions.append(line)
            rom_address += 1

    # 第二次掃描：轉成 16 位元二進位碼
    machine_code = []
    next_ram_address = 16

    for inst in instructions:
        if inst.startswith("@"):
            symbol = inst[1:]
            if symbol.isdigit():
                address = int(symbol)
            else:
                if symbol not in symbols:
                    symbols[symbol] = next_ram_address
                    next_ram_address += 1
                address = symbols[symbol]
            machine_code.append(f"0{address:015b}")
        else:
            dest, comp, jump = "", inst, ""
            if "=" in comp:
                dest, comp = comp.split("=")
            if ";" in comp:
                comp, jump = comp.split(";")
            machine_code.append(f"111{COMP_TABLE[comp]}{DEST_TABLE[dest]}{JUMP_TABLE[jump]}")

    output_path = os.path.splitext(input_path)[0] + ".hack"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(machine_code) + "\n")
    print(f"成功產生: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方式: python HackAssembler.py <檔案路徑.asm>")
        sys.exit(1)
    assemble(sys.argv[1])
