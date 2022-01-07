check: test todo

test:
	nose2 --with-coverage

todo:
	@rgrep --include "*.py" "TODO" || true
	@rgrep --include "*.py" "REF" || true
