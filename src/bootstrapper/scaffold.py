from __future__ import annotations

import json
from pathlib import Path


DEFAULT_UNITY_VERSION = "6000.0.0f1"


def create_unity_project_files(output_dir: Path, manifest: dict, install_packages: bool = False) -> list[Path]:
    created: list[Path] = []
    for directory in manifest.get("directories", []):
        path = output_dir / directory
        path.mkdir(parents=True, exist_ok=True)
        created.append(path)

    project_version = output_dir / "ProjectSettings" / "ProjectVersion.txt"
    _write(project_version, f"m_EditorVersion: {DEFAULT_UNITY_VERSION}\nm_EditorVersionWithRevision: {DEFAULT_UNITY_VERSION}\n")
    created.append(project_version)

    project_settings = output_dir / "ProjectSettings" / "ProjectSettings.asset"
    _write(
        project_settings,
        "%YAML 1.1\n--- !u!129 &1\nPlayerSettings:\n  productGUID: 00000000000000000000000000000000\n",
    )
    created.append(project_settings)

    readme = output_dir / "Assets" / "_Project" / "README.md"
    _write(
        readme,
        "# Unity Project Structure\n\nThis scaffold was generated from `conductor/project-brief.md`.\n",
    )
    created.append(readme)

    template_files = _write_unity_templates(output_dir, manifest)
    created.extend(template_files)

    package_manifest = output_dir / "Packages" / "manifest.json"
    dependencies = {}
    if install_packages:
        dependencies.update(_unity_package_versions(manifest.get("unity_packages", [])))
    _write(
        package_manifest,
        json.dumps({"dependencies": dependencies}, indent=2, ensure_ascii=False) + "\n",
    )
    created.append(package_manifest)

    packages_lock = output_dir / "Packages" / "packages-lock.json"
    _write(packages_lock, json.dumps({"dependencies": {}}, indent=2) + "\n")
    created.append(packages_lock)

    verification_config = output_dir / ".orchestrator" / "verification.json"
    _write(
        verification_config,
        json.dumps(
            {
                "commands": [],
                "notes": [
                    "Add project-specific commands here, for example Unity batchmode tests or Python tooling checks.",
                    "The `unity-ai verify` command reads this file when no --command is provided.",
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
    )
    created.append(verification_config)

    performance_rules = output_dir / ".orchestrator" / "rules" / "performance-rules.json"
    _write(
        performance_rules,
        json.dumps(
            {
                "rules": [
                    {
                        "id": "unity.hotpath.lookup",
                        "category": "cpu",
                        "severity": "high",
                        "description": "Avoid GetComponent, GameObject.Find, and FindObjectOfType in Update-like methods.",
                    },
                    {
                        "id": "unity.hotpath.allocation",
                        "category": "gc",
                        "severity": "high",
                        "description": "Avoid managed allocations in Update, FixedUpdate, and LateUpdate.",
                    },
                    {
                        "id": "unity.lifecycle.instantiate-destroy",
                        "category": "object_lifecycle",
                        "severity": "medium",
                        "description": "Use object pools for repeated gameplay Instantiate/Destroy patterns.",
                    },
                    {
                        "id": "unity.physics.hotpath-query",
                        "category": "physics",
                        "severity": "medium",
                        "description": "Cache layer masks and reduce physics query frequency in hot paths.",
                    },
                ]
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
    )
    created.append(performance_rules)

    return created


def _write_unity_templates(output_dir: Path, manifest: dict) -> list[Path]:
    created: list[Path] = []
    project_name = _sanitize_identifier(manifest.get("project_name", "UnityAIProject"))
    namespace = project_name
    templates = {
        "Assets/_Project/Runtime/Runtime.asmdef": json.dumps(
            {
                "name": f"{project_name}.Runtime",
                "rootNamespace": namespace,
                "references": [],
                "includePlatforms": [],
                "excludePlatforms": [],
                "allowUnsafeCode": False,
                "overrideReferences": False,
                "precompiledReferences": [],
                "autoReferenced": True,
                "defineConstraints": [],
                "versionDefines": [],
                "noEngineReferences": False,
            },
            indent=2,
        )
        + "\n",
        "Assets/_Project/Editor/Editor.asmdef": json.dumps(
            {
                "name": f"{project_name}.Editor",
                "rootNamespace": f"{namespace}.Editor",
                "references": [f"{project_name}.Runtime"],
                "includePlatforms": ["Editor"],
                "excludePlatforms": [],
                "allowUnsafeCode": False,
                "overrideReferences": False,
                "precompiledReferences": [],
                "autoReferenced": True,
                "defineConstraints": [],
                "versionDefines": [],
                "noEngineReferences": False,
            },
            indent=2,
        )
        + "\n",
        "Assets/_Project/Tests/RuntimeTests.asmdef": json.dumps(
            {
                "name": f"{project_name}.Tests",
                "rootNamespace": f"{namespace}.Tests",
                "references": [f"{project_name}.Runtime"],
                "includePlatforms": ["Editor"],
                "excludePlatforms": [],
                "allowUnsafeCode": False,
                "overrideReferences": False,
                "precompiledReferences": [],
                "autoReferenced": True,
                "defineConstraints": [],
                "versionDefines": [],
                "noEngineReferences": False,
            },
            indent=2,
        )
        + "\n",
        "Assets/_Project/Runtime/Core/GameState.cs": _game_state(namespace),
        "Assets/_Project/Runtime/Core/GameBootstrap.cs": _game_bootstrap(namespace),
        "Assets/_Project/Runtime/Gameplay/PlayerController.cs": _player_controller(namespace),
        "Assets/_Project/Runtime/Gameplay/EnemySpawner.cs": _enemy_spawner(namespace),
        "Assets/_Project/Runtime/Infrastructure/EventBus.cs": _event_bus(namespace),
        "Assets/_Project/Runtime/Infrastructure/ObjectPool.cs": _object_pool(namespace),
        "Assets/_Project/Tests/EditMode/BootstrapSmokeTest.cs": _bootstrap_smoke_test(namespace),
        "Assets/_Project/Scenes/Main.unity": _minimal_scene_yaml(),
    }
    for relative, content in templates.items():
        path = output_dir / relative
        _write(path, content)
        created.append(path)
    return created


def _sanitize_identifier(value: str) -> str:
    cleaned = "".join(character if character.isalnum() else "_" for character in value)
    if not cleaned or cleaned[0].isdigit():
        cleaned = f"UnityProject_{cleaned}"
    return cleaned


def _game_state(namespace: str) -> str:
    return f"""namespace {namespace}.Core
{{
    public enum GameState
    {{
        Boot,
        Playing,
        Paused,
        GameOver
    }}
}}
"""


def _game_bootstrap(namespace: str) -> str:
    return f"""using UnityEngine;

namespace {namespace}.Core
{{
    public sealed class GameBootstrap : MonoBehaviour
    {{
        [SerializeField] private GameState initialState = GameState.Boot;

        public GameState CurrentState {{ get; private set; }}

        private void Awake()
        {{
            CurrentState = initialState;
            Application.targetFrameRate = 60;
        }}

        public void SetState(GameState nextState)
        {{
            CurrentState = nextState;
        }}
    }}
}}
"""


def _player_controller(namespace: str) -> str:
    return f"""using UnityEngine;

namespace {namespace}.Gameplay
{{
    [RequireComponent(typeof(CharacterController))]
    public sealed class PlayerController : MonoBehaviour
    {{
        [SerializeField] private float moveSpeed = 5f;

        private CharacterController characterController;
        private Transform cachedTransform;

        private void Awake()
        {{
            characterController = GetComponent<CharacterController>();
            cachedTransform = transform;
        }}

        private void Update()
        {{
            float horizontal = Input.GetAxisRaw("Horizontal");
            float vertical = Input.GetAxisRaw("Vertical");
            Vector3 direction = new Vector3(horizontal, 0f, vertical);
            if (direction.sqrMagnitude > 1f)
            {{
                direction.Normalize();
            }}

            characterController.SimpleMove(cachedTransform.TransformDirection(direction) * moveSpeed);
        }}
    }}
}}
"""


def _enemy_spawner(namespace: str) -> str:
    return f"""using {namespace}.Infrastructure;
using UnityEngine;

namespace {namespace}.Gameplay
{{
    public sealed class EnemySpawner : MonoBehaviour
    {{
        [SerializeField] private ObjectPool enemyPool;
        [SerializeField] private Transform spawnPoint;

        public void SpawnOne()
        {{
            if (enemyPool == null || spawnPoint == null)
            {{
                return;
            }}

            GameObject enemy = enemyPool.Get();
            enemy.transform.SetPositionAndRotation(spawnPoint.position, spawnPoint.rotation);
        }}
    }}
}}
"""


def _event_bus(namespace: str) -> str:
    return f"""using System;
using System.Collections.Generic;

namespace {namespace}.Infrastructure
{{
    public sealed class EventBus
    {{
        private readonly Dictionary<Type, Delegate> handlers = new Dictionary<Type, Delegate>();

        public void Subscribe<TEvent>(Action<TEvent> handler)
        {{
            Type eventType = typeof(TEvent);
            handlers[eventType] = handlers.TryGetValue(eventType, out Delegate existing)
                ? Delegate.Combine(existing, handler)
                : handler;
        }}

        public void Publish<TEvent>(TEvent gameEvent)
        {{
            if (handlers.TryGetValue(typeof(TEvent), out Delegate handler))
            {{
                ((Action<TEvent>)handler)?.Invoke(gameEvent);
            }}
        }}
    }}
}}
"""


def _object_pool(namespace: str) -> str:
    return f"""using System.Collections.Generic;
using UnityEngine;

namespace {namespace}.Infrastructure
{{
    public sealed class ObjectPool : MonoBehaviour
    {{
        [SerializeField] private GameObject prefab;
        [SerializeField] private int initialSize = 16;

        private readonly Queue<GameObject> pool = new Queue<GameObject>();

        private void Awake()
        {{
            for (int index = 0; index < initialSize; index++)
            {{
                GameObject instance = CreateInstance();
                instance.SetActive(false);
                pool.Enqueue(instance);
            }}
        }}

        public GameObject Get()
        {{
            GameObject instance = pool.Count > 0 ? pool.Dequeue() : CreateInstance();
            instance.SetActive(true);
            return instance;
        }}

        public void Return(GameObject instance)
        {{
            instance.SetActive(false);
            pool.Enqueue(instance);
        }}

        private GameObject CreateInstance()
        {{
            return Instantiate(prefab, transform);
        }}
    }}
}}
"""


def _bootstrap_smoke_test(namespace: str) -> str:
    return f"""using {namespace}.Core;
using NUnit.Framework;

namespace {namespace}.Tests
{{
    public sealed class BootstrapSmokeTest
    {{
        [Test]
        public void GameStateContainsBootState()
        {{
            Assert.AreEqual(0, (int)GameState.Boot);
        }}
    }}
}}
"""


def _minimal_scene_yaml() -> str:
    return """%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!29 &1
OcclusionCullingSettings:
  m_ObjectHideFlags: 0
--- !u!104 &2
RenderSettings:
  m_ObjectHideFlags: 0
  m_Fog: 0
--- !u!157 &3
LightmapSettings:
  m_ObjectHideFlags: 0
--- !u!196 &4
NavMeshSettings:
  serializedVersion: 2
"""


def _unity_package_versions(packages: list[str]) -> dict[str, str]:
    versions = {
        "com.unity.inputsystem": "1.7.0",
        "com.unity.render-pipelines.universal": "17.0.3",
        "com.unity.addressables": "2.2.2",
    }
    return {package: versions.get(package, "latest") for package in packages}


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
