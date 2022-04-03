package main

import (
	"bytes"
	"fmt"
	"os"
	"os/exec"
	"runtime"
	"strings"
)

func main() {
	var branch string

	remote, err := getRemote()
	if err != nil {
		fmt.Println("this is not a git repository")
		return
	}

	repository := getRepositoryInfoFromRemote(remote)
	if repository == "" {
		fmt.Println("unable to get repositoru name from remote url")
		return
	}

	// at least one argument is given
	if len(os.Args) > 1 {
		branch = os.Args[1]
	} else {
		branch = currentBranch()
	}

	err = isValidBranch(branch)
	if err != nil {
		fmt.Println(err)
		return
	}

	url := buildURL(remote, repository, branch)
	if url == "" {
		fmt.Println("unable to build URL for repository")
		return
	}

	open(url)
}

func currentBranch() string {
	cmd := exec.Command("git", "rev-parse", "--abbrev-ref", "HEAD")

	var out bytes.Buffer
	cmd.Stdout = &out

	err := cmd.Run()
	if err != nil {
		fmt.Println(err)
		return ""
	}

	return strings.TrimSpace(out.String())
}

func isValidBranch(branch string) error {
	cmd := exec.Command("git", "branch", "-r")

	var out bytes.Buffer
	cmd.Stdout = &out

	err := cmd.Run()
	if err != nil {
		return err
	}

	if !strings.Contains(out.String(), "origin/"+branch) {
		return fmt.Errorf("branch '%s' does not exist on remote", branch)
	}

	return nil
}

func getRemote() (string, error) {
	cmd := exec.Command("git", "config", "remote.origin.url")

	var out bytes.Buffer
	cmd.Stdout = &out

	if err := cmd.Run(); err != nil {
		return "", err
	}

	return strings.TrimSpace(out.String()), nil
}

func getRepositoryInfoFromRemote(remote string) string {
	if strings.Contains(remote, "http") {
		if strings.Contains(remote, ".com/") {
			return strings.Split(remote, ".com/")[1]
		}
		if strings.Contains(remote, ".org/") {
			return strings.Split(remote, ".org/")[1]
		}
	} else {
		return strings.Split(remote, ":")[1]
	}

	return ""
}

func buildURL(remote string, repository string, branch string) string {
	// remove the .git from the repository path
	repository = strings.Split(repository, ".git")[0]

	if strings.Contains(remote, "github") {
		return "https://github.com/" + repository + "/tree/" + branch
	}

	if strings.Contains(remote, "bitbucket") {
		return "https://bitbucket.org/" + repository + "/branch/" + branch
	}

	if strings.Contains(remote, "gitlab") {
		return "https://gitlab.com/" + repository + "/tree/" + branch
	}

	return ""
}

func open(path string) {
	os := runtime.GOOS
	switch os {
	case "darwin":
		exec.Command("open", path).Run()
	case "linux":
		exec.Command("xdg-open", path).Run()
	default:
		fmt.Printf("sorry, I don't know how to open it with %s\n", os)
	}
}
