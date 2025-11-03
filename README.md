# Shared Document Network デモ

このディレクトリには、共有ドキュメントmodの機能を完全に実演するデモが含まれており、複数のエージェントがリアルタイムでドキュメントの作成、編集、レビューに協力する方法を示しています。

## デモ概要

このデモでは以下を実演します：

1. **ドキュメント作成**: エディターエージェントが新しい共有ドキュメントを作成
2. **共同編集**: 複数のエージェントが同時に異なる部分を編集
3. **レビューとコメント**: レビューアーエージェントがフィードバックと提案を追加
4. **プレゼンス追跡**: エージェントがお互いの作業位置を追跡
5. **ドキュメント管理**: コンテンツ、履歴の表示、およびドキュメントの管理

## ファイル

- `network.yaml`: デモ用のネットワーク設定
- `editor_agent.yaml`: ドキュメントエディターエージェントの設定
- `reviewer_agent.yaml`: ドキュメントレビューアーエージェントの設定
- `collaborator_agent.yaml`: 共同作業エージェントの設定
- `demo_script.py`: メインの実演スクリプト
- `simple_demo.py`: 簡易版デモスクリプト（モックネットワークを使用）
- `README.md`: このドキュメントファイル

## 前提条件

1. OpenAgentsがインストールされ、設定されていること
2. Python 3.8+ と必要な依存関係
3. OpenAI API キー（`OPENAI_API_KEY`環境変数として設定）

## デモの実行

1. **環境変数の設定**:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

2. **デモの実行**:
   ```bash
   cd shared_document_network
   python demo_script.py
   ```

3. **共同作業の観察**:
   スクリプトは各エージェントの動作を詳細な出力で示しながら、様々な共有ドキュメント操作を実演します。

## デモシナリオ

### シナリオ1: ドキュメント作成
- エディターエージェントが新しい「Project Requirements」ドキュメントを作成
- プレースホルダーセクション付きの初期コンテンツを設定
- 他のエージェントに読み書き権限を付与

### シナリオ2: 共同編集
- 複数のエージェントが同じドキュメントを開く
- エディターがスコープセクションを更新
- 共同作業者が詳細なタイムライン情報を追加
- エディターがリソース割り当ての詳細を追加
- すべての変更がリアルタイムで同期される

### シナリオ3: レビューとコメント
- レビューアーエージェントがドキュメントを開く
- 特定の行に建設的なコメントを追加
- コンテンツの品質と完全性に関するフィードバックを提供
- コメントは特定の行番号に添付される

### シナリオ4: プレゼンス追跡
- エージェントがカーソル位置を更新
- システムが誰がドキュメントのどこで作業しているかを追跡
- 他のエージェントがアクティブな共同作業者とその位置を確認可能

### シナリオ5: ドキュメント管理
- コメント付きの現在のドキュメントコンテンツを取得
- すべての変更を確認するための操作履歴を表示
- 利用可能なドキュメントの一覧表示
- ドキュメントアクセスと権限の管理

## 期待される出力

デモは詳細なコンソール出力を生成し、以下を示します：

```
🎯 Starting Shared Document Collaboration Demo
============================================================
🚀 Setting up shared document collaboration network...
✅ Network started successfully
👥 Creating demonstration agents...
✅ All agents created and started

📝 Demo 1: Document Creation
--------------------------------------------------
Editor creating new document...
Document creation result: {'status': 'success', 'message': "Document creation request sent for 'Project Requirements'"}

🤝 Demo 2: Collaborative Editing
--------------------------------------------------
Agents opening document...
Editor updating scope section...
Collaborator adding timeline details...
Editor adding resource information...

💬 Demo 3: Review and Comments
--------------------------------------------------
Reviewer opening document for review...
Reviewer adding feedback comments...

👀 Demo 4: Agent Presence Tracking
--------------------------------------------------
Agents updating their working positions...
Checking agent presence...

📋 Demo 5: Document Management
--------------------------------------------------
Getting current document content...
Getting document operation history...
Listing all available documents...

🎉 Demo completed successfully!
============================================================
```

## カスタマイズ

以下の方法でデモをカスタマイズできます：

1. **エージェント設定の変更**: YAMLファイルを編集してエージェントの性格や機能を変更
2. **ドキュメントコンテンツの変更**: `demo_script.py`の初期コンテンツを更新
3. **エージェントの追加**: 追加のエージェント設定を作成し、デモに追加
4. **シナリオの拡張**: 新しいデモ関数を追加して追加機能を実演

## トラブルシューティング

### よくある問題

1. **ネットワーク接続エラー**: 
   - 他のサービスがポート8700を使用していないことを確認してください
   - エージェント設定ファイル（`editor_agent.yaml`など）のポート番号が`network.yaml`の設定と一致していることを確認してください（デフォルトは8700）

2. **認証エラー**:
   - 開発環境では、`network.yaml`に`disable_agent_secret_verification: true`を追加して認証を無効化できます
   - 本番環境ではこの設定を削除または`false`に設定してください

3. **エージェント登録失敗**: エージェント設定が有効であることを確認してください

4. **OpenAI API エラー**: APIキーが正しく設定されていることを確認してください

5. **権限エラー**: エージェントが適切なアクセス権限を持っていることを確認してください

### デバッグモード

ネットワーク設定を変更してデバッグログを有効化：

```yaml
log_level: "DEBUG"
```

### 手動テスト

個別の操作を手動でテストすることもできます：

```python
# 簡単なテストを作成
import asyncio
from openagents.utils.agent_loader import load_agent_from_yaml

async def test_basic_operations():
    agent, connection = load_agent_from_yaml("editor_agent.yaml")
    await agent.async_start(
        network_host=connection.get("host", "localhost") if connection else "localhost",
        network_port=connection.get("port", 8700) if connection else 8700,
        network_id=connection.get("network_id") if connection else None
    )
    
    # ドキュメントを作成
    documents_adapter = agent.get_mod_adapter("openagents.mods.workspace.documents")
    if documents_adapter:
        result = await documents_adapter.create_document(
            document_name="Test Doc",
            initial_content="Hello World"
        )
        print(f"Create result: {result}")
    
    await agent.async_stop()

asyncio.run(test_basic_operations())
```

## 統合例

共有ドキュメントmodは、様々なユースケースに統合できます：

1. **コードレビューシステム**: インラインコメント付きの共同コードレビュー
2. **ドキュメント作成**: リアルタイム編集による複数著者によるドキュメント作成
3. **プロジェクト計画**: 共同要件および計画ドキュメント
4. **ナレッジ管理**: 専門家による貢献を含む共有ナレッジベース
5. **コンテンツ作成**: 共同執筆および編集ワークフロー

このデモは、OpenAgents共有ドキュメントmodを使用して、より複雑な共同ドキュメントシステムを構築するための基盤を提供します。

## 設定ファイルの説明

### network.yaml
ネットワークの設定ファイルです。以下の主要な設定が含まれています：
- **ポート設定**: HTTPポート8700、gRPCポート8600
- **セキュリティ設定**: 開発環境では`encryption_enabled: false`、`disable_agent_secret_verification: true`を推奨
- **Mod設定**: 共有ドキュメント、メッセージング、フォーラム、Wikiなどのmodが有効化されています

### エージェント設定ファイル（editor_agent.yaml, reviewer_agent.yaml, collaborator_agent.yaml）
各エージェントの設定を含んでいます：
- **agent_id**: エージェントの一意の識別子
- **config**: モデル名、プロバイダー、指示文などの設定
- **mods**: 有効化するmodのリスト（`openagents.mods.workspace.documents`が必須）
- **connection**: ネットワーク接続情報（ホスト、ポート、ネットワークID）

**重要**: エージェント設定ファイルのポート番号は`network.yaml`のHTTPポート（デフォルト8700）と一致させる必要があります。
