#!/usr/bin/env python3

# Code Map
# '항목 코드' :  [
# 				1. 수집스크립트 함수명, 2. 수집스크립트 실행 코드,
# 				3. 항목 분류, 4. 항목명,
# 				5. 항목중요도, 6. 항목중요도 점수,
# 				7. 판단기준,
# 				8. 조치방법
# 				]

linuxUcodeMap = {
	'U-01':
		[
			['linux001', 'linux001 U-01'],
			[
				'계정 관리', 'root 계정 원격 접속 제한',
				'상', '3',
				'양호: 원격 터미널 서비스를 사용하지 않거나, 사용 시 root 직접 접속을 차단한 경우\n'
				'취약: 원격 터미널 서비스 사용 시 root 직접 접속을 허용한 경우',
				'원격 접속 시 root 계정으로 바로 접속 할 수 없도록 설정파일 수정'
			]
		],
	'U-03':
		[
			['linux003', 'linux003 U-03'],
			[
				'계정 관리', '계정 잠금 임계값 설정',
				'상', '3',
				'양호: 계정 잠금 임계값이 5 이하의 값으로 설정되어 있는 경우\n'
				'취약: 계정 잠금 임계값이 설정되어 있지 않거나, 5 이하의 값으로 설정되지 않은 경우',
				'계정 잠금 임계값을 5 이하로 설정'
			]
		],
	'U-07':
		[
			['linux007', 'linux007 U-07'],
			[
				'파일 및 디렉터리 관리', '/etc/passwd 파일 소유자 및 권한 설정',
				'상', '3',
				'양호: /etc/passwd 파일 소유자가 root이고, 권한이 644 이하인 경우\n'
				'취약: /etc/passwd 파일 소유자가 root가 아니거나, 권한이 644 이하가 아닌 경우',
				'/etc/passwd 파일 소유자 및 권한 변경 (소유자 root, 권한 644)'
			]
		],
	'U-08':
		[
			['linux008', 'linux008 U-08'],
			[
				'파일 및 디렉터리 관리', '/etc/shadow 파일 소유자 및 권한 설정',
				'상', '3',
				'양호: /etc/shadow 파일 소유자가 root이고, 권한이 400 이하인 경우\n'
				'취약: /etc/shadow 파일 소유자가 root가 아니거나, 권한이 400 이하가 아닌 경우',
				'/etc/shadow 파일 소유자 및 권한 변경 (소유자 root, 권한 400)'
			]
		],
	'U-31':
		[
			['linux031', 'linux031 U-31'],
			[
				'서비스 관리', '스팸 메일 릴레이 제한',
				'상', '3',
				'양호: SMTP 서비스를 사용하지 않거나 릴레이 제한이 설정되어 있는 경우\n'
				'취약: SMTP 서비스를 사용하며 릴레이 제한이 설정되어 있지 않은 경우',
				'Sendmail 서비스를 사용하지 않을 경우 서비스 중지, 사용할 경우 릴레이 방지 설정 또는, 릴레이 대상 접근 제어'
			]
		],
	'U-32':
		[
			['linux032', 'linux032 U-32'],
			[
				'서비스 관리', '일반사용자의 Sendmail 실행 방지',
				'상', '3',
				'양호: SMTP 서비스 미사용 또는, 일반 사용자의 Sendmail 실행 방지가 설정된 경우\n'
				'취약: SMTP 서비스 사용 및 일반 사용자의 Sendmail 실행 방지가 설정되어 있지 않은 경우',
				'Sendmail 서비스를 사용하지 않을 경우 서비스 중지\n'
				'Sendmail 서비스를 사용 시 sendmail.cf 설정파일에 restrictqrun 옵션 추가 설정'
			]
		],
	'U-42':
		[
			['linux042', 'linux042 U-42'],
			[
				'패치 관리', '최신 보안패치 및 벤더 권고사항 적용',
				'상', '3',
				'양호: 패치 적용 정책을 수립하여 주기적으로 패치를 관리하고 있는 경우\n'
				'취약: 패치 적용 정책을 수립하지 않고 주기적으로 패치관리를 하지 않는 경우',
				'OS 관리자, 서비스 개발자가 패치 적용에 따른 서비스 영향 정도를 파악하여 OS 관리자 및 벤더에서 적용함'
			]
		],
	'U-43':
		[
			['linux043', 'linux043 U-43'],
			[
				'로그 관리', '로그의 정기적 검토 및 보고',
				'상', '3',
				'양호: 로그 기록의 검토, 분석, 리포트 작성 및 보고 등이 정기적으로 이루어지는 경우\n'
				'취약: 로그 기록의 검토, 분석, 리포트 작성 및 보고 등이 정기적으로 이루어지지 않는 경우',
				'로그 기록 검토 및 분석을 시행하여 리포트를 작성하고 정기적으로 보고함'
			]
		],
}
