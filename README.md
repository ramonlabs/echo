# Echo

A Live2D AI VTuber built as a microservices monorepo.

## Services

| Service                                                 | Access  | License |
| ------------------------------------------------------- | ------- | ------- |
| [tts](https://github.com/ramonlabs/echo-tts)            | public  | GPL 2.0 |
| [stt](https://github.com/ramonlabs/echo-stt)            | public  | GPL 2.0 |
| [panel](https://github.com/ramonlabs/echo-panel)        | private |         |
| [llm](https://github.com/ramonlabs/echo-llm)            | private |         |
| [avatar](https://github.com/ramonlabs/echo-avatar)      | private |         |
| [memory](https://github.com/ramonlabs/echo-memory)      | private |         |
| [training](https://github.com/ramonlabs/echo-training)  | private |         |

> [!NOTE]
> The private submodules are not publicly accessible. This is intentional.

## Setup

```bash
git clone git@github.com:ramonlabs/echo.git
cd echo
git submodule update --init services/tts services/stt
uv sync
```
