class mechanism:
	LOWEST_LEVEL = 0
	LOW_LEVEL = 1
	HIGH_LEVEL_GMAC = 5
	HIGH_LEVEL_ECDSA = 7

class sc_byte:
	NO_SECURITY = 0x00
	AUTH_ONLY = 0x10
	ENCRYPT_ONLY = 0x20
	AUTH_ENCRYPT = 0x30

class sec_policy:
	REQ_CHECK = 28
	RESP_CHECK = 224

	AUTH_CHECK = 36
	ENC_CHECK = 72