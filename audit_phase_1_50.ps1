Write-Host "========================================"
Write-Host "FORGEHACKS PHASE 1-50 AUDIT"
Write-Host "========================================"
Write-Host ""

Write-Host "=== GIT STATUS ==="
git status --short
Write-Host ""

Write-Host "=== BRANCH ==="
git branch --show-current
Write-Host ""

Write-Host "=== GIT LOG ==="
git --no-pager log --oneline --decorate -15
Write-Host ""

Write-Host "=== PROJECT FILES ==="
Get-ChildItem -Recurse -File |
    Where-Object {
        $_.FullName -notmatch '\\.venv\\' -and
        $_.FullName -notmatch '\\__pycache__\\' -and
        $_.FullName -notmatch '\\.git\\'
    } |
    Sort-Object FullName |
    ForEach-Object {
        $_.FullName.Replace((Get-Location).Path + "\", "")
    }
Write-Host ""

Write-Host "=== PYTHON COMPILE CHECK ==="
python -m compileall -q src tests
if ($LASTEXITCODE -eq 0) {
    Write-Host "COMPILE: PASS"
} else {
    Write-Host "COMPILE: FAIL"
}
Write-Host ""

Write-Host "=== PYTEST ==="
pytest -q
Write-Host ""

Write-Host "=== DEPENDENCY CHECK ==="
python -m pip check
Write-Host ""

Write-Host "=== SECRET SCAN ==="
$patterns = @(
    "FEATHERLESS_API_KEY\s*=\s*[^`r`n]+",
    "OPENAI_API_KEY\s*=\s*[^`r`n]+",
    "GEMINI_API_KEY\s*=\s*[^`r`n]+",
    "sk-[A-Za-z0-9_-]+"
)

$files = Get-ChildItem -Recurse -File |
    Where-Object {
        $_.FullName -notmatch '\\.venv\\' -and
        $_.FullName -notmatch '\\__pycache__\\' -and
        $_.FullName -notmatch '\\.git\\'
    }

$secretFound = $false

foreach ($file in $files) {
    try {
        $content = Get-Content $file.FullName -Raw -ErrorAction Stop

        foreach ($pattern in $patterns) {
            if ($content -match $pattern) {
                Write-Host "POTENTIAL SECRET: $($file.FullName)"
                $secretFound = $true
            }
        }
    }
    catch {
        # Ignore binary/unreadable files.
    }
}

if (-not $secretFound) {
    Write-Host "SECRET SCAN: CLEAN"
}

Write-Host ""

Write-Host "=== MUTABLE DEFAULT CHECK ==="
$mutableMatches = Get-ChildItem src -Recurse -Filter *.py |
    Select-String -Pattern '=\s*\{\}|=\s*\[\]' |
    Where-Object {
        $_.Line -notmatch 'assert' -and
        $_.Line -notmatch '=='
    }

if ($mutableMatches) {
    $mutableMatches | ForEach-Object {
        Write-Host "$($_.Path):$($_.LineNumber): $($_.Line.Trim())"
    }
} else {
    Write-Host "MUTABLE DEFAULT CHECK: CLEAN"
}

Write-Host ""

Write-Host "=== IMPORT CHECK ==="
python -c "import src.config; import src.environment; import src.schemas; import src.pipeline; import src.json_parser; import src.prompt_templates; import src.prompt_manager; import src.prompt_safety; import src.llm_client; import src.logger; import src.orchestrator; import src.retriever; import src.rag; import src.tools; import src.tool_catalog; import src.tool_executor; import src.agent; import src.agent_schema; import src.agent_decision; import src.agent_prompts; import src.agent_decision_maker; import src.agent_loop; import src.agent_result; import src.agent_safety; import src.evaluation; import src.evaluator; import src.benchmark; import src.benchmark_runner; import src.evaluation_summary; import src.cache; import src.api; print('IMPORT CHECK: PASS')"
Write-Host ""

Write-Host "========================================"
Write-Host "AUDIT COMPLETE"
Write-Host "========================================"
