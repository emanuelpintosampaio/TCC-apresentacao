# Apresentação do TCC

Slides da defesa do TCC *Avaliação de Simplificações do Modelo Físico e de Métodos de Integração Temporal Aplicados à Difusão de Gás em Gotículas Marinha*, de Emanuel Pinto Sampaio (Matemática Industrial, UFES, 2026).

**Abrir a apresentação:** https://emanuelpintosampaio.github.io/TCC-apresentacao/

Use as setas do teclado ou a barra de espaço para avançar os slides. O código, os resultados e o texto do TCC estão no repositório [TCC](https://github.com/emanuelpintosampaio/TCC).

## Código em Manim

Os slides foram feitos com [Manim Community](https://www.manim.community/) e [manim-slides](https://github.com/jeertmans/manim-slides). O código está na pasta `manim/`:

| Arquivo | O que é |
|---|---|
| `apresentacao.py` | Código da apresentação publicada: cenas `Titulo`, `Agenda` e `Introducao` (esta última tem todo o restante, com as seções marcadas por comentários) |
| `bbbb.py` | Pseudocódigo do algoritmo multiescala, exibido num dos slides (não é Python executável) |
| `imagens/` | Figuras e gráficos usados nos slides |
| `manim.cfg` | Diz ao Manim que as imagens estão em `imagens/` |

Para gerar os slides de novo é preciso ter Manim, manim-slides, mscene e LaTeX. No Ubuntu:

```bash
sudo apt install texlive dvisvgm                         # LaTeX
pip install manim "manim-slides[pyside6-full]" mscene
mscene plugins
```

Depois, de dentro da pasta `manim/`:

```bash
manim -ql apresentacao.py Titulo Agenda Introducao              # qualidade baixa (a dos slides publicados)
manim-slides convert Titulo Agenda Introducao apresentacao.html # gera o HTML
manim-slides present Titulo Agenda Introducao                   # apresenta em tela cheia
```

O vídeo do último slide (`apresentacao_assets/video.mp4`) não é gerado pelo Manim. É uma cópia comprimida (1080p, 30 quadros por segundo) do original, que tinha 607 MB e passava do limite de 100 MB por arquivo do GitHub.
