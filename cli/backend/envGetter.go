package backend

import (
	"os"
	"errors"
	"github.com/joho/godotenv"
)

type CLIData struct {
	Secret string
	APIURL string
}

func LoadENV() (CLIData, error) {
	responseData := CLIData{
		Secret: "",
		APIURL: "",
	}

	err := godotenv.Load()
	if err != nil {
		return responseData, err
	}

	code := os.Getenv("SECRET_CODE")
	apiUrl := os.Getenv("API_URL")

	if code == "" {
		return responseData, errors.New("secret code is not loaded")
	}

	if apiUrl == "" {
		return responseData, errors.New("api url is not loaded")
	}
	responseData.APIURL = apiUrl
	responseData.Secret = code
	return responseData, nil
}
