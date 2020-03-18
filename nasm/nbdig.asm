;	Task:
;Take an integer n (n >= 0) and a digit d (0 <= d <= 9) as an integer. 
;Square all numbers k (0 <= k <= n) between 0 and n. 
;Count the numbers of digits d used in the writing of all the k**2. 
;Call nb_dig (or nbDig or ...) the function taking n and d as parameters and returning this count.
	section .bss		; секция для директив резевной памяти
count:	resd 1			; переменная для хранения результата
n:	resd 1			; переменная для цикла
	section .text		; секция кода
	global nbdig		; создаем запись о функции nbdig
nbdig:				; реализуем эту функцию
	push ebp		; стандартный пролог
	mov ebp, esp		;
	mov [count], dword 0	; инициализируем счетчик
	mov [n], dword 0	; инициализируем переменную для цикла

.number_loop:			
	mov eax, [n]		; кладем в rax число
	mul eax			; rax*rax
	call count_digits	; вызываем count_digits
	add [count], eax	; добавляем к count кол-во единиц в прошлом числе
	inc dword [n]		; увеличиваем переменную n на 1
	cmp [n], edi		; проверяем не перешли ли мы за границу(проверяем с n,по условию задачи)
	jle .number_loop	; продолжаем цикл,если <=

	mov eax, [count]	; помещаем в rax указатель на массив результата
	mov esp, ebp		; стандартный конец главной функции
	pop ebp
	ret	

count_digits:
	mov ecx, 0		; каждый раз обнуляем счетчик d 
	mov ebx, 10		; делитель

.while_loop:
	xor edx, edx 		; обнуляем rdx,куда залетает остаток от деления
	div ebx			; делим rax на 10
	cmp edx, esi		; сравниваем остаток с d,по условию задачи
	jne .digit_not_found	; если не равны,то переходим снова к делению на 10

	inc ecx

.digit_not_found:
	test eax, eax		; проверяем условие продолжения while_loop
	jnz .while_loop		; если не ноль,продолжаем выполнять while_loop

	mov eax, ecx		; иначе кладём в rax кол-во единиц,в текущем числе
	ret
