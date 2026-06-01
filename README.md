[README(1).md](https://github.com/user-attachments/files/27500634/README.1.md)

# 💀 RogueHacker

> *"Toda porta é uma proposição. Todo movimento é uma prova."*

Um dungeon crawler roguelike no terminal onde você **invade salas de servidores** usando **lógica proposicional** como mecânica central de segurança.

---

## 🧠 Conceito

Você é um hacker rogue navegando por uma rede de servidores gerada proceduralmente. Cada sala é um nó. Cada porta é uma porta lógica. Cada run é uma nova topologia.

A dungeon não é fantasia — é **infraestrutura**. Suas armas são exploits. Suas chaves são credenciais. Seus inimigos são daemons antivírus.

---

## 🎮 Mecânicas Principais

| Elemento | Descrição |
|---|---|
| **Salas** | Salas de servidores dispostas em grid de dungeon |
| **Portas** | Travadas por condições de lógica proposicional |
| **Exploits** | Coletáveis que alternam estados booleanos |
| **Antivírus** | Inimigos de patrulha que disparam alarmes |
| **Alarmes** | Alteram o estado da sala — invalidam condições das portas |

### Exemplo de Porta Lógica

```
A = Credencial obtida
B = Firewall desativado
C = Alarme ligado

Porta ROOT:  (A ∧ B) ∧ ¬C
```

Você só entra na ROOT se tiver a credencial, o firewall desligado **e** o alarme silencioso.

Cada porta do jogo é uma **fórmula em lógica proposicional**. Seu inventário é uma **atribuição de verdade**.

---

## 🛠️ Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.x |
| Renderização | `curses` / `rich` |
| Arquitetura | A definir |
| Plataforma | Terminal (cross-platform) |

---

## 📐 Contexto Acadêmico

**Disciplina:** (Lógica matemática para computação)
**Período:** 3B — 2026.1
**Tópicos aplicados:**
- Lógica Proposicional
- Álgebra Booleana
- Estruturas condicionais
- Máquinas de estado

---

## 🗺️ Funcionalidades Planejadas

- [ ] Geração procedural de dungeon
- [ ] Sistema de portas por lógica proposicional
- [ ] Inventário de exploits (gerenciamento de estado booleano)
- [ ] IA de patrulha do antivírus
- [ ] Propagação de estado de alarme
- [ ] Múltiplos arquétipos de servidor (ROOT, SHADOW, VAULT...)
- [ ] Interface terminal com painéis `rich`

---

## 🚀 Como Executar

```bash
git clone https://github.com/SEU_USUARIO/RogueHacker
cd RogueHacker
python main.py
```

> Requisitos: Python 3.10+ · biblioteca `rich`

```bash
pip install rich
```

---

## 📁 Estrutura (planejada)

```
RogueHacker/
├── main.py
├── core/
│   ├── dungeon.py       # Geração de salas/mapa
│   ├── logic.py         # Avaliador proposicional
│   ├── player.py        # Estado e inventário
│   └── entities.py      # Antivírus, alarmes
├── ui/
│   └── renderer.py      # Renderização curses / rich
└── README.md
```

---

## ⚖️ Licença

Proprietário — uso acadêmico exclusivo.
Todos os direitos reservados © 2026.
