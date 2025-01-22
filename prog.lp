\ Model PROG
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  V22 + V23 + V24 + V25 + V26 + V27 + V28 + V29 + V30
Subject To
 C34: V0 <= 200
 C35: V1 <= 200
 C36: V2 <= 200
 C37: V3 <= 200
 C38: V7 <= 200
 C39: V8 <= 200
 C40: V9 <= 200
 C41: - V4 <= -50
 C42: - V5 <= -100
 C43: - V6 <= -50
 C44: - V0 + V13 <= 0
 C45: V14 <= 0
 C46: - 0.5 V0 + V15 <= 0
 C47: - V1 + V16 <= 0
 C48: - V1 + V17 <= 0
 C49: - V1 + V18 <= 0
 C50: - V2 + V19 <= 0
 C51: - V2 + V20 <= 0
 C52: - V2 + V21 <= 0
 C53: - V3 + V10 <= 0
 C54: - V3 + V11 <= 0
 C55: - V3 + V12 <= 0
 C31: - 10 V13 - 10 V14 - 10 V15 + V28 = 0
 C32: - 50 V16 - 50 V17 - 50 V18 + V29 = 0
 C33: V30 = 0
 C56: - 5000 V0 + V22 = 0
 C57: - 1000 V1 + V23 = 0
 C58: V24 = 0
 C59: - 500 V0 + V25 = 0
 C60: - 100 V1 + V26 = 0
 C61: V27 = 0
 C62: - V7 + V13 = 0
 C63: - V8 + V14 = 0
 C64: - V9 + V15 = 0
 C65: - V4 + V13 - V16 + V19 = 0
 C66: - V5 + V14 - V17 + V20 = 0
 C67: - V6 + V15 - V18 + V21 = 0
 C68: - V10 + V16 - V19 = 0
 C69: V10 - V11 + V17 - V20 = 0
 C70: V11 - V12 + V18 - V21 = 0
Bounds
End
