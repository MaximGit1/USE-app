package main

import (
	"admin/utils/backend"
	"fmt"
	"os"
)

type Command struct {
	title string
	args []string
}

func NewCommand(title string, agrs []string) Command {
	return Command{
		title: title,
		args: agrs,
	}
}


func main() {
	data, err := backend.LoadENV()
	if err != nil {
		fmt.Println(err)
		return
	}
	args := os.Args
	if len(args) == 1 {
		showListCommands()
		return
	}

	switch args[1] {
	case "create-admin":
		username := args[2]
		password := args[3]
		userInput := backend.UserInput{
			Username: username,
			Password: password,
		}

		result, err := backend.CreateUserAdmin(userInput, data)
		if err != nil {
			fmt.Print(err)
			return
		}
		fmt.Println(result)
		return
	default:
		showListCommands()
	}
}


func showListCommands() {
	fmt.Println("admin-cli <command> <arg> <arg> ...")
	fmt.Println()
	var commands []Command

	createAdminCommand := NewCommand("create-admin", []string{"<username>", "<password>"})

	commands = append(commands, createAdminCommand)

	i := 1
	for _, command := range commands {
		argsInRow := ""
		for _, arg := range command.args {
			argsInRow += arg + " "
		}
		fmt.Printf("%v. %v %v", i, command.title, argsInRow)
		i++
	}
}
