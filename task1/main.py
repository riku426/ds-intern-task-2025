import sys
import json

def solve():
    # 標準入力から1行ずつ読み取り、カンマで分割した結果を「rows」に格納
    rows = []
    for line in sys.stdin:
        line = line.strip()
        # 空行はスキップ
        if not line:
            continue
        row = line.split(',')
        rows.append(row)

    # 「規格」行を探す（行頭が「規格」の行）
    spec_row_index = None
    for i, row in enumerate(rows):
        if row and row[0] == "規格":
            spec_row_index = i
            break

    # 規格行の 1 列目以降が規格名となる
    specs = rows[spec_row_index][1:]

    # 規格行より上の行は共通情報として辞書にまとめる
    shared_fields = {}
    for row in rows[:spec_row_index]:
          key = row[0]
          value = row[1]
          # "-" は無値扱い → 辞書に含めない
          if value != "-":
              shared_fields[key] = value

    # 規格行より下をdetails_rowsとして扱う
    detail_rows = rows[spec_row_index + 1 :]

    # 項目名（例: "量", "定植", "備考"）→ 各規格列の値一覧
    details_map = {}

    for row in detail_rows:
        if not row:
            continue
        item_name = row[0]  # 例: "量", "定植", "備考"

        # item_name に対応する値（規格ごと）
        raw_values = row[1:]

        # 左から右へ走査して空文字を左の値で埋める（セル結合を再現）
        for idx in range(1, len(raw_values)):
            if raw_values[idx] == "":
                raw_values[idx] = raw_values[idx - 1]

        # 規格数より列数が少ない場合、最後の値を右に延長する
        if len(raw_values) < len(specs):
            last_val = raw_values[-1] if raw_values else ""
            raw_values += [last_val] * (len(specs) - len(raw_values))

        details_map[item_name] = raw_values

    # JSON出力用にリストを作成
    result = []

    for i, spec in enumerate(specs):
        entry = {}
        # まず共通情報をコピー
        for k, v in shared_fields.items():
            entry[k] = v

        # 規格をセット
        entry["規格"] = spec

        # 詳細情報をまとめる
        detail_dict = {}
        for item_name, values in details_map.items():
            val = values[i]
            # "-" は値が無い扱いなのでスキップ
            if val != "-" and val.strip() != "":
                detail_dict[item_name] = val

        entry["詳細"] = detail_dict
        result.append(entry)

    # JSON として出力
    print(json.dumps(result, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    solve()
