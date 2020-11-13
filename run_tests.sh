for d in ./*/ ; do (cd "$d" && (printf "\n\nStudent username: ${d:2:-1}, pytest output:\n") && pytest); done

