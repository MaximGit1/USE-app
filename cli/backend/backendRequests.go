package backend

import (
	"bytes"
	"crypto/tls"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"time"
)

type UserInput struct {
	Username string `json:"username"`
	Password string `json:"password"`
}


func CreateUserAdmin(userData UserInput, cliData CLIData) (string, error) {
	userID, err := registerUser(userData, cliData)
	if err != nil {
		return "", fmt.Errorf("registration failed: %v", err)
	}

	err = updateUserRole(userID, cliData)
	if err != nil {
		return "", fmt.Errorf("role update failed: %v", err)
	}

	return fmt.Sprintf("Successfully created admin user with ID: %d", userID), nil
}

func registerUser(userData UserInput, cliData CLIData) (uint32, error) {
	url := cliData.APIURL + "/auth/register/"

	jsonData, err := json.Marshal(userData)
	if err != nil {
		return 0, errors.New("invalid user data")
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return 0, err
	}

	setCommonHeaders(req)
	tr := &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    }

    client := &http.Client{
        Transport: tr,
        Timeout:   10 * time.Second,
    }

	resp, err := client.Do(req)
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusCreated {
		return 0, fmt.Errorf("unexpected status: %d", resp.StatusCode)
	}

	var result struct {
		UserID uint32 `json:"user_id"`
	}

	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return 0, fmt.Errorf("failed to parse response: %v", err)
	}

	return result.UserID, nil
}

func updateUserRole(userID uint32, cliData CLIData) error {
    url := fmt.Sprintf("%s/users/%d/update/role", cliData.APIURL, userID)

    jsonData, err := json.Marshal("admin")
    if err != nil {
        return fmt.Errorf("failed to marshal role data: %v", err)
    }

    req, err := http.NewRequest("PATCH", url, bytes.NewBuffer(jsonData))
    if err != nil {
        return fmt.Errorf("failed to create request: %v", err)
    }

    setCommonHeaders(req)

    tr := &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    }

    client := &http.Client{
        Transport: tr,
        Timeout:   10 * time.Second,
        CheckRedirect: func(req *http.Request, via []*http.Request) error {
            return http.ErrUseLastResponse
        },
    }

    resp, err := client.Do(req)
    if err != nil {
        return fmt.Errorf("request failed: %v", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        body, _ := io.ReadAll(resp.Body)
        return fmt.Errorf("unexpected status [%d]: %s", resp.StatusCode, string(body))
    }

    return nil
}


func setCommonHeaders(req *http.Request) {
	req.Header.Set("Content-Type", "application/json")
}
