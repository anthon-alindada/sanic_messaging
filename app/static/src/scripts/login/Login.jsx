// Core
import React from 'react'
import Cookies from 'js-cookie'
import axios from 'axios'
import debounce from 'debounce'

// Component
import {
  Text,
  Box,
  Grid,
  Button,
  Grommet,
  TextInput,
} from 'grommet'


// Theme
const theme = {
  global: {
    font: {
      family: 'Lato',
    },
  },
  button: {
    border: {
      radius: undefined,
      color: '#2196f3',
    },
    primary: {
      color: '#2196f3',
    },
  },
}


class Login extends React.Component {
  state = {
    emailInput: '',
    passwordInput: '',
    loggingIn: false,
    loginError: {
      message: '',
      data: {},
    },
  }

  login = debounce((email, password) => {
    // Create login axios request
    const loginApi = axios.create({
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'x-csrf-token': Cookies.get('csrf_token'),
      },
    })

    loginApi.post('/api/login', {
      email,
      password,
    }).then(() => {
      // If login success redirect
      window.location.assign('/')
    }).catch((error) => {
      // If login failed
      this.setState({
        loginError: error.response.data.errors,
        loggingIn: false,
      })
    })
  }, 1000)

  onEmailInputChange = (event) => {
    this.setState({
      emailInput: event.target.value,
    })
  }

  onPasswordInputChange = (event) => {
    this.setState({
      passwordInput: event.target.value,
    })
  }

  onLoginFormSubmit = (event) => {
    event.preventDefault()

    // Remove errors and set logging in
    this.setState({
      loginError: {
        message: '',
        data: {},
      },
      loggingIn: true,
    })

    // Get inputs
    const {
      emailInput,
      passwordInput,
    } = this.state

    // Login
    this.login(
      emailInput,
      passwordInput,
    )
  }

  renderError = () => {
    const {
      loginError: {
        message: errorMessage,
      },
    } = this.state

    if (errorMessage) {
      return (
        <strong>
          <Text
            color="status-critical"
            className="error-message"
          >
            {errorMessage}
          </Text>
        </strong>
      )
    }

    return null
  }

  render() {
    const {
      emailInput,
      passwordInput,
      loggingIn,
    } = this.state

    return (
      <Grommet theme={theme} full>
        <Box align="center" justify="center">
          <div className="login-box">
            <h1 className="login-head">Login</h1>

            {this.renderError()}

            <form
              method="POST"
              action="/login"
              onSubmit={this.onLoginFormSubmit}
              className="login-form"
            >
              <Grid
                columns={{
                  count: 1,
                  size: 'auto',
                }}
                gap="small"
              >
                <Box>
                  <TextInput
                    id="email-input"
                    name="email"
                    placeholder="Email address"
                    value={emailInput}
                    onChange={this.onEmailInputChange}
                  />
                </Box>
              </Grid>

              <Grid
                columns={{
                  count: 1,
                  size: 'auto',
                }}
                gap="small"
              >
                <Box>
                  <TextInput
                    id="password-input"
                    name="password"
                    type="password"
                    placeholder="Password"
                    value={passwordInput}
                    onChange={this.onPasswordInputChange}
                  />
                </Box>
              </Grid>

              <Grid
                columns={{
                  count: 1,
                  size: 'auto',
                }}
                gap="small"
              >
                <Box>
                  <Button
                    primary
                    label="Login"
                    type="submit"
                    className="login-button"
                    disabled={loggingIn}
                    onClick={() => {}}
                  />
                </Box>
              </Grid>
            </form>
          </div>
        </Box>
      </Grommet>
    )
  }
}

export default Login
