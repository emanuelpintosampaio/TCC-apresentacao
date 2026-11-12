# Apresentação do TCC

Slides da defesa do TCC *Avaliação de Simplificações do Modelo Físico e de Métodos de Integração Temporal Aplicados à Difusão de Gás em Gotículas Marinha*, de Emanuel Pinto Sampaio (Matemática Industrial, UFES, 2026).

### [Acesse o site](https://emanuelpintosampaio.github.io/TCC-apresentacao/)

https://emanuelpintosampaio.github.io/TCC-apresentacao/

O site conta a pesquisa como uma história. Uma gotícula sai da crista de uma onda, absorve CO₂ do ar e volta para o mar levando o gás. Depois vêm o impacto, a física da gotícula, a pesquisa (as duas iniciações científicas e o TCC), os métodos, os resultados, a conclusão, os slides da defesa e os materiais. Funciona no computador e no celular, sem instalar nada.

Nos slides, use as setas para avançar e voltar, a barra de espaço para pausar e `F` para tela cheia. Os mesmos slides também estão na [versão clássica](https://emanuelpintosampaio.github.io/TCC-apresentacao/apresentacao(2).html). O código, os resultados e o texto do TCC estão no repositório [TCC](https://github.com/emanuelpintosampaio/TCC).

## Rodar o código no Google Colab

Para gerar os slides a partir do código sem instalar nada no computador, abra o notebook no Colab e rode as três células:

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/emanuelpintosampaio/TCC-apresentacao/blob/main/rodar_no_colab.ipynb)

O notebook instala o Manim, o LaTeX, o manim-slides e o mscene, gera os slides e mostra a apresentação dentro do próprio Colab. A instalação leva uns 5 minutos, e a geração dos slides, de 10 a 20 minutos.

## Código em Manim

Os slides foram feitos com [Manim Community](https://www.manim.community/) e [manim-slides](https://github.com/jeertmans/manim-slides). O código está na pasta `manim/`:

| Arquivo | O que é |
|---|---|
| `apresentacao.py` | Código da apresentação publicada: cenas `Titulo`, `Agenda` e `Introducao` (esta última tem todo o restante, com as seções marcadas por comentários) |
| `bbbb.py` | Pseudocódigo do algoritmo multiescala, exibido num dos slides (não é Python executável) |
| `imagens/` | Figuras e gráficos usados nos slides |
| `manim.cfg` | Diz ao Manim que as imagens estão em `imagens/` |

## Gerar os slides no computador

É preciso ter Manim, manim-slides, mscene e LaTeX. O Manim tem que ser anterior à versão 0.22, porque o manim-slides 5.7 ainda não funciona com ela.

### Linux (Ubuntu)

```bash
sudo apt install texlive dvisvgm                         # LaTeX
pip install "manim<0.22" "manim-slides[pyside6-full]" mscene
mscene plugins
```

### Windows

1. **Baixe o repositório.** Em [github.com/emanuelpintosampaio/TCC-apresentacao](https://github.com/emanuelpintosampaio/TCC-apresentacao), clique em **Code → Download ZIP** e extraia. Se tiver o [Git](https://git-scm.com/download/win), pode usar `git clone https://github.com/emanuelpintosampaio/TCC-apresentacao.git`.
2. **Instale o LaTeX (MiKTeX).** Baixe em [miktex.org/download](https://miktex.org/download) e instale. Na opção *Install missing packages on-the-fly*, escolha **Yes**, para ele baixar sozinho os pacotes que o Manim pedir.
3. **Instale o uv** (gerenciador de Python). Abra o **PowerShell** e rode:

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   Feche e abra o PowerShell de novo.
4. **Instale as bibliotecas.** No PowerShell, entre na pasta do repositório e rode:

   ```powershell
   uv venv --python 3.12
   .venv\Scripts\activate
   uv pip install "manim<0.22" "manim-slides[pyside6-full]" mscene
   mscene plugins
   ```

   Se o PowerShell disser que a execução de scripts está desabilitada, rode `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e tente o `activate` de novo. Se a instalação pedir o Microsoft Visual C++, instale as [Build Tools do Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/) com a opção *Desenvolvimento para desktop com C++*, abra um PowerShell novo e repita o `uv pip install`.

Nas próximas vezes, basta entrar na pasta do repositório e rodar `.venv\Scripts\activate` antes dos comandos abaixo.


### Gerar e apresentar

De dentro da pasta `manim/` (no Windows e no Linux):

```bash
manim -ql apresentacao.py Titulo Agenda Introducao              # gera os vídeos (qualidade baixa, a dos slides publicados)
manim-slides convert Titulo Agenda Introducao apresentacao.html # gera o HTML
manim-slides present Titulo Agenda Introducao                   # apresenta em tela cheia
```

Para qualidade alta, troque `-ql` por `-qh`. Na primeira vez no Windows, o MiKTeX baixa os pacotes de LaTeX que faltarem, então demora mais.

O vídeo do último slide (`apresentacao_assets/video.mp4`) não é gerado pelo Manim. É uma cópia comprimida (1080p, 30 quadros por segundo) do original, que tinha 607 MB e passava do limite de 100 MB por arquivo do GitHub.
