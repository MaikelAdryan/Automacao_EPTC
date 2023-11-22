test = ['PCA PEREIRA PAROBE , 888 - CENTRO HISTORIC',
 'AV TOLEDO PIZA , 8888 - SARANDI',
 'AV TOLEDO PIZA , 000 - indefinido',
 'R JACOB PHILIPPSEN , 000 - indefinido',
 'AV BRASILIANO INDIO DE MORAES , 000 - indefinido',
 'AV ASSIS BRASIL , 000 - indefinido',
 'PCA RUI BARBOSA , 000 - indefinido',
 'AV ASSIS BRASIL , 00 - indefinido',
 'AV SERTORIO , 00 - indefinido',
 'R VINTE QUATRO DE OUTUBRO , 888 - MOINHOS VENTO',
 'AV SOUZA MELO , 000 - indefinido',
 'AV ASSIS BRASIL , 1818 - PASSO DA AREIA'
 ]


remove = '00 - indefinido'
for i in test:
	print(i.split(' ,')[0])

