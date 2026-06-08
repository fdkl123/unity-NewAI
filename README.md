# AI Engineering Orchestrator for Unity Games

Languages: [中文](#中文) | [English](#english) | [日本語](#日本語) | [한국어](#한국어)

---

## 中文

AI Engineering Orchestrator 是面向 Unity 项目的 AI 工程编排平台。当前第一入口是 **AI Unity Project Bootstrapper**：它会先通过问诊理解游戏想法，分析项目类型、风险、技术架构和所需 AI 技能，用户确认后才生成 Unity + AI 开发脚手架上下文。

### 当前已实现

- `unity-ai new` 新项目问诊流程。
- 项目类型、首个可玩版本、架构候选、风险和非目标分析。
- AI 技能解析，例如 `spec`、`unity-developer`、`unity-performance`、`memory-management`。
- 生成前确认预览。
- 确认后生成 `project-brief.md`、`ai-skills.md`、`scaffold-manifest.json` 等上下文文件。

### 环境要求

- Python `3.11+`
- 当前 Bootstrapper MVP 无运行时第三方依赖。

### 快速开始

```powershell
python -m unittest discover -s tests
```

Dry run，不写入文件：

```powershell
$env:PYTHONPATH="src"
python -m bootstrapper.cli new --non-interactive `
  --project-name ArenaPrototype `
  --idea "Mobile 3D roguelike action arena with enemy waves." `
  --dimension 3D `
  --platforms Android,iOS `
  --core-action "Move, dodge, and fight waves of enemies." `
  --first-playable "movement,basic combat,enemy spawning,one arena" `
  --team solo `
  --ai-help planning,code,performance,tests
```

确认并生成项目上下文：

```powershell
$env:PYTHONPATH="src"
python -m bootstrapper.cli new --non-interactive --confirm `
  --output-dir ./out/ArenaPrototype `
  --project-name ArenaPrototype `
  --idea "Mobile 3D roguelike action arena with enemy waves." `
  --dimension 3D `
  --platforms Android,iOS `
  --core-action "Move, dodge, and fight waves of enemies." `
  --first-playable "movement,basic combat,enemy spawning,one arena" `
  --team solo `
  --ai-help planning,code,performance,tests
```

### 生成文件

- `conductor/project-brief.md`
- `conductor/ai-skills.md`
- `conductor/architecture-decision.md`
- `conductor/risk-register.md`
- `conductor/mvp-plan.md`
- `conductor/performance-budget.md`
- `scaffold-manifest.json`
- `.orchestrator/bootstrapper-session.json`

### 主要流程

```text
游戏想法
→ 核心问诊
→ 项目诊断
→ 技能解析
→ 架构推荐
→ 风险登记
→ 项目确认预览
→ 用户确认
→ 脚手架清单和上下文文件
```

### 验证流水线

`unity-ai verify` 支持两种方式：

```powershell
$env:PYTHONPATH="src"
python -m bootstrapper.cli verify --project-dir ./out/ArenaPrototype --command "python --version"
```

或读取 `.orchestrator/verification.json`：

```json
{
  "commands": [
    "python --version"
  ]
}
```

```powershell
$env:PYTHONPATH="src"
python -m bootstrapper.cli verify --project-dir ./out/ArenaPrototype
```

### 当前状态

已实现：`unity-ai new` CLI、条件式第二轮问诊、确定性诊断、技能解析、确认预览、上下文文件生成、Unity 工程脚手架文件生成、基础 C# 模板、asmdef、示例 Scene、Unity package manifest 写入、已有 Unity 项目扫描、静态性能分析器、Markdown/JSON 报告、验证流水线 runner、单元测试。

未实现：Unity Editor 自动启动、Unity Package Manager 在线解析、Profiler 数据导入、AST 级 C# 自动修复、可视化 UI。

---

## English

AI Engineering Orchestrator is an agentic engineering platform for Unity projects. Its first entry point is the **AI Unity Project Bootstrapper**: it asks targeted questions, understands the game idea, diagnoses project type, risk, architecture, and required AI skills, then generates Unity + AI scaffold context only after user confirmation.

### Implemented Now

- `unity-ai new` onboarding flow for a new Unity game idea.
- Diagnosis for project type, first playable scope, architecture candidates, risks, and non-goals.
- AI skill resolution for skills such as `spec`, `unity-developer`, `unity-performance`, and `memory-management`.
- Confirmation preview before writing files.
- Confirmed artifact generation including `project-brief.md`, `ai-skills.md`, and `scaffold-manifest.json`.

### Requirements

- Python `3.11+`
- No runtime third-party dependencies for the current Bootstrapper MVP.

### Quick Start

```powershell
python -m unittest discover -s tests
```

Dry run without writing files:

```powershell
$env:PYTHONPATH="src"
python -m bootstrapper.cli new --non-interactive `
  --project-name ArenaPrototype `
  --idea "Mobile 3D roguelike action arena with enemy waves." `
  --dimension 3D `
  --platforms Android,iOS `
  --core-action "Move, dodge, and fight waves of enemies." `
  --first-playable "movement,basic combat,enemy spawning,one arena" `
  --team solo `
  --ai-help planning,code,performance,tests
```

Confirm and write project artifacts:

```powershell
$env:PYTHONPATH="src"
python -m bootstrapper.cli new --non-interactive --confirm `
  --output-dir ./out/ArenaPrototype `
  --project-name ArenaPrototype `
  --idea "Mobile 3D roguelike action arena with enemy waves." `
  --dimension 3D `
  --platforms Android,iOS `
  --core-action "Move, dodge, and fight waves of enemies." `
  --first-playable "movement,basic combat,enemy spawning,one arena" `
  --team solo `
  --ai-help planning,code,performance,tests
```

### Generated Files

- `conductor/project-brief.md`
- `conductor/ai-skills.md`
- `conductor/architecture-decision.md`
- `conductor/risk-register.md`
- `conductor/mvp-plan.md`
- `conductor/performance-budget.md`
- `scaffold-manifest.json`
- `.orchestrator/bootstrapper-session.json`

### Main Workflow

```text
Game idea
→ Core questionnaire
→ Project diagnosis
→ Skill resolution
→ Architecture recommendation
→ Risk register
→ Project brief preview
→ User confirmation
→ Scaffold manifest and context artifacts
```

### Verification Pipeline

`unity-ai verify` supports direct commands:

```powershell
$env:PYTHONPATH="src"
python -m bootstrapper.cli verify --project-dir ./out/ArenaPrototype --command "python --version"
```

Or `.orchestrator/verification.json`:

```json
{
  "commands": [
    "python --version"
  ]
}
```

```powershell
$env:PYTHONPATH="src"
python -m bootstrapper.cli verify --project-dir ./out/ArenaPrototype
```

### Current Status

Implemented: `unity-ai new` CLI, conditional second-round questionnaire, deterministic diagnosis, skill resolution, confirmation preview, artifact generation, Unity scaffold file generation, basic C# templates, asmdef files, sample Scene, Unity package manifest writing, existing Unity project scanner, static performance analyzer, Markdown/JSON reports, verification runner, and unit tests.

Not implemented yet: automatic Unity Editor launch, online Unity Package Manager resolution, Profiler data ingestion, AST-level C# auto-fixes, and visual UI.

---

## 日本語

AI Engineering Orchestrator は Unity プロジェクト向けの AI エンジニアリング編成プラットフォームです。最初の入口は **AI Unity Project Bootstrapper** です。ゲーム案を質問形式で整理し、プロジェクト種別、リスク、技術アーキテクチャ、必要な AI スキルを分析し、ユーザー確認後に Unity + AI 開発用のコンテキストとスキャフォールド情報を生成します。

### 現在実装済み

- 新規 Unity ゲーム案向けの `unity-ai new` オンボーディング。
- プロジェクト種別、最初のプレイ可能範囲、アーキテクチャ候補、リスク、非対象範囲の診断。
- `spec`、`unity-developer`、`unity-performance`、`memory-management` などの AI スキル解決。
- ファイル生成前の確認プレビュー。
- `project-brief.md`、`ai-skills.md`、`scaffold-manifest.json` などの成果物生成。

### 必要環境

- Python `3.11+`
- 現在の Bootstrapper MVP には実行時の外部依存関係はありません。

### クイックスタート

```powershell
python -m unittest discover -s tests
```

ファイルを書き込まない dry run:

```powershell
$env:PYTHONPATH="src"
python -m bootstrapper.cli new --non-interactive `
  --project-name ArenaPrototype `
  --idea "Mobile 3D roguelike action arena with enemy waves." `
  --dimension 3D `
  --platforms Android,iOS `
  --core-action "Move, dodge, and fight waves of enemies." `
  --first-playable "movement,basic combat,enemy spawning,one arena" `
  --team solo `
  --ai-help planning,code,performance,tests
```

確認して成果物を書き込む:

```powershell
$env:PYTHONPATH="src"
python -m bootstrapper.cli new --non-interactive --confirm `
  --output-dir ./out/ArenaPrototype `
  --project-name ArenaPrototype `
  --idea "Mobile 3D roguelike action arena with enemy waves." `
  --dimension 3D `
  --platforms Android,iOS `
  --core-action "Move, dodge, and fight waves of enemies." `
  --first-playable "movement,basic combat,enemy spawning,one arena" `
  --team solo `
  --ai-help planning,code,performance,tests
```

### 生成ファイル

- `conductor/project-brief.md`
- `conductor/ai-skills.md`
- `conductor/architecture-decision.md`
- `conductor/risk-register.md`
- `conductor/mvp-plan.md`
- `conductor/performance-budget.md`
- `scaffold-manifest.json`
- `.orchestrator/bootstrapper-session.json`

### 主な流れ

```text
ゲーム案
→ コア質問
→ プロジェクト診断
→ スキル解決
→ アーキテクチャ推奨
→ リスク登録
→ プロジェクト確認プレビュー
→ ユーザー確認
→ スキャフォールド manifest とコンテキスト成果物
```

### 現在の状態

実装済み: `unity-ai new` CLI、条件分岐の第 2 回質問、決定的な診断、スキル解決、確認プレビュー、成果物生成、Unity スキャフォールドファイル生成、基本 C# テンプレート、asmdef、サンプル Scene、Unity package manifest 書き込み、既存 Unity プロジェクトスキャナー、静的パフォーマンス分析器、Markdown/JSON レポート、検証 runner、単体テスト。

未実装: Unity Editor の自動起動、Unity Package Manager のオンライン解決、Profiler データ取り込み、AST レベルの C# 自動修正、ビジュアル UI。

---

## 한국어

AI Engineering Orchestrator는 Unity 프로젝트를 위한 에이전트형 엔지니어링 플랫폼입니다. 첫 진입점은 **AI Unity Project Bootstrapper**입니다. 게임 아이디어를 질문으로 구체화하고, 프로젝트 유형, 리스크, 기술 아키텍처, 필요한 AI 스킬을 분석한 뒤, 사용자가 확인한 후에만 Unity + AI 개발 스캐폴드 컨텍스트를 생성합니다.

### 현재 구현된 기능

- 새 Unity 게임 아이디어를 위한 `unity-ai new` 온보딩 플로우.
- 프로젝트 유형, 첫 플레이 가능 범위, 아키텍처 후보, 리스크, 비목표 범위 진단.
- `spec`, `unity-developer`, `unity-performance`, `memory-management` 같은 AI 스킬 해석.
- 파일 생성 전 확인 프리뷰.
- `project-brief.md`, `ai-skills.md`, `scaffold-manifest.json` 등 산출물 생성.

### 요구 사항

- Python `3.11+`
- 현재 Bootstrapper MVP에는 런타임 외부 의존성이 없습니다.

### 빠른 시작

```powershell
python -m unittest discover -s tests
```

파일을 쓰지 않는 dry run:

```powershell
$env:PYTHONPATH="src"
python -m bootstrapper.cli new --non-interactive `
  --project-name ArenaPrototype `
  --idea "Mobile 3D roguelike action arena with enemy waves." `
  --dimension 3D `
  --platforms Android,iOS `
  --core-action "Move, dodge, and fight waves of enemies." `
  --first-playable "movement,basic combat,enemy spawning,one arena" `
  --team solo `
  --ai-help planning,code,performance,tests
```

확인 후 산출물 생성:

```powershell
$env:PYTHONPATH="src"
python -m bootstrapper.cli new --non-interactive --confirm `
  --output-dir ./out/ArenaPrototype `
  --project-name ArenaPrototype `
  --idea "Mobile 3D roguelike action arena with enemy waves." `
  --dimension 3D `
  --platforms Android,iOS `
  --core-action "Move, dodge, and fight waves of enemies." `
  --first-playable "movement,basic combat,enemy spawning,one arena" `
  --team solo `
  --ai-help planning,code,performance,tests
```

### 생성 파일

- `conductor/project-brief.md`
- `conductor/ai-skills.md`
- `conductor/architecture-decision.md`
- `conductor/risk-register.md`
- `conductor/mvp-plan.md`
- `conductor/performance-budget.md`
- `scaffold-manifest.json`
- `.orchestrator/bootstrapper-session.json`

### 주요 흐름

```text
게임 아이디어
→ 핵심 질문
→ 프로젝트 진단
→ 스킬 해석
→ 아키텍처 추천
→ 리스크 등록
→ 프로젝트 확인 프리뷰
→ 사용자 확인
→ 스캐폴드 manifest 및 컨텍스트 산출물
```

### 현재 상태

구현됨: `unity-ai new` CLI, 조건부 2차 질문, 결정적 진단, 스킬 해석, 확인 프리뷰, 산출물 생성, Unity 스캐폴드 파일 생성, 기본 C# 템플릿, asmdef, 샘플 Scene, Unity package manifest 작성, 기존 Unity 프로젝트 스캐너, 정적 성능 분석기, Markdown/JSON 보고서, 검증 runner, 단위 테스트.

아직 미구현: Unity Editor 자동 실행, Unity Package Manager 온라인 해석, Profiler 데이터 수집, AST 수준 C# 자동 수정, 시각적 UI.
