num = 0

print("\n🎲 Bem-vindo ao jogo dos Números da Sorte! 🎲")
print("Você terá 3 chances para tentar a sorte. Digite um número por vez.\n")

for i in range(3):
    try:

        num = int(input("\nDigite um número Inteiro por vez: "))

        if num < 18:
            print(f"\nO número escolhido foi {num} ele me diz que você vai ter sorte amanhã!")
        
        elif 18 <= num >= 22:
            print(f"\n✅ O número escolhido foi {num} e ele é um dos números de sorte do dia")
            print("\n🎁 Você recebeu R$ 15 de crédito na sua próxima compra!")
               
        else:
            print(f"\n❌ O número escolhido foi {num} e ele não vai te dar sorte hoje!")
            print("\nTente novamente")

    except ValueError:
        print("\nEntrada inválida! por favor, digite paenas números válidos!")

print("\n✨ Obrigado por jogar! Espero você amanhã! ✨")
