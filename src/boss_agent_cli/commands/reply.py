from __future__ import annotations

import click

from boss_agent_cli.auth.manager import AuthManager
from boss_agent_cli.compliance import require_compliance_allowed
from boss_agent_cli.commands._contact_lookup import resolve_friend_or_emit
from boss_agent_cli.commands._platform import get_platform_instance
from boss_agent_cli.display import handle_auth_errors, handle_error_output, handle_output


@click.command("reply")
@click.argument("uid_or_security_id")
@click.argument("message")
@click.option("--dry-run", is_flag=True, help="仅核对目标联系人，不发送")
@click.pass_context
@handle_auth_errors("reply")
def reply_cmd(ctx: click.Context, uid_or_security_id: str, message: str, dry_run: bool) -> None:
	"""在求职者聊天页向指定联系人发送后续消息。"""
	if not require_compliance_allowed(ctx, "reply"):
		ctx.exit(1)

	auth = AuthManager(ctx.obj["data_dir"], logger=ctx.obj["logger"], platform=ctx.obj.get("platform", "zhipin"))
	with get_platform_instance(ctx, auth) as platform:
		friend = resolve_friend_or_emit(ctx, "reply", platform, uid_or_security_id)
		if friend is None:
			return
		data = {
			"uid": str(friend.get("uid", "")),
			"name": friend.get("name", ""),
			"company": friend.get("brandName") or friend.get("brand_name") or "",
			"message": message,
			"dry_run": dry_run,
		}
		if dry_run:
			handle_output(ctx, "reply", data)
			return
		result = platform.reply(str(friend.get("uid", "")), message)
		if not isinstance(result, dict) or not result.get("ok"):
			handle_error_output(ctx, "reply", code="ACTION_UNCONFIRMED", message=(result or {}).get("error", "消息发送未确认"), recoverable=False, details=result or {})
			return
		handle_output(ctx, "reply", {**data, "sent": True, "page_result": result})
