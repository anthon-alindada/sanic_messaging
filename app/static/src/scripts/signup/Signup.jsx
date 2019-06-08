// Core
import React from 'react'
import camelcaseKeys from 'camelcase-keys'
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


class Signup extends React.Component {
  state = {
    emailInput: '',
    lastNameInput: '',
    firstNameInput: '',
    passwordInput: '',
    confirmPasswordInput: '',
    signingUp: false,
    signupError: {
      data: {},
      message: '',
    },
  }

  signup = debounce((
    email,
    lastName,
    firstName,
    password,
    confirmPassword,
  ) => {
    // Create signup axios request
    const signupApi = axios.create({
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'x-csrf-token': Cookies.get('csrf_token'),
      },
    })

    signupApi.post('/api/signup', {
      email,
      first_name: firstName,
      last_name: lastName,
      password,
      confirm_password: confirmPassword,
    }).then(() => {
      // If signup success redirect
      window.location.assign('/')
    }).catch((error) => {
      // If signup failed
      this.setState({
        signupError: camelcaseKeys(error.response.data.errors, { deep: true }),
        signingUp: false,
      })
    })
  }, 1000)

  onEmailInputChange = (event) => {
    this.setState({
      emailInput: event.target.value,
    })
  }

  onFirstNameInputChange = (event) => {
    this.setState({
      firstNameInput: event.target.value,
    })
  }

  onLastNameInputChange = (event) => {
    this.setState({
      lastNameInput: event.target.value,
    })
  }

  onPasswordInputChange = (event) => {
    this.setState({
      passwordInput: event.target.value,
    })
  }

  onConfirmPasswordInputChange = (event) => {
    this.setState({
      confirmPasswordInput: event.target.value,
    })
  }

  onSignupFormSubmit = (event) => {
    event.preventDefault()

    // Remove errors and set signing up
    this.setState({
      signupError: {
        message: '',
        data: '',
      },
      signingUp: true,
    })

    // Get inputs
    const {
      emailInput,
      lastNameInput,
      firstNameInput,
      passwordInput,
      confirmPasswordInput,
    } = this.state

    // Signup
    this.signup(
      emailInput,
      lastNameInput,
      firstNameInput,
      passwordInput,
      confirmPasswordInput,
    )
  }

  renderError = (field) => {
    const {
      signupError: {
        data: signupErrorData,
      },
    } = this.state

    if (signupErrorData[field]) {
      return (
        <Text
          color="status-critical"
          size="small"
          className="error-message"
        >
          {signupErrorData[field]}
        </Text>
      )
    }

    return null
  }

  render() {
    const {
      emailInput,
      firstNameInput,
      lastNameInput,
      passwordInput,
      confirmPasswordInput,
      signupError: {
        data: signupErrors,
      },
      signingUp,
    } = this.state

    return (
      <Grommet theme={theme} full>
        <Box align="center" justify="center">
          <div className="signup-box">
            <h1 className="signup-head">Create new account</h1>

            <form
              method="POST"
              action="/signup"
              onSubmit={this.onSignupFormSubmit}
              className="signup-form"
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
                    className={signupErrors.email ? 'error' : ''}
                    onChange={this.onEmailInputChange}
                  />

                  {this.renderError('email')}
                </Box>
              </Grid>

              <Grid
                columns={{
                  count: 2,
                  size: 'auto',
                }}
                gap="small"
              >
                <Box>
                  <TextInput
                    id="first-name-input"
                    name="first_name"
                    placeholder="First name"
                    value={firstNameInput}
                    className={signupErrors.firstName ? 'error' : ''}
                    onChange={this.onFirstNameInputChange}
                  />

                  {this.renderError('firstName')}
                </Box>

                <Box>
                  <TextInput
                    id="last-name-input"
                    name="last_name"
                    placeholder="Last name"
                    value={lastNameInput}
                    className={signupErrors.lastName ? 'error' : ''}
                    onChange={this.onLastNameInputChange}
                  />

                  {this.renderError('lastName')}
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
                    className={signupErrors.password ? 'error' : ''}
                    onChange={this.onPasswordInputChange}
                  />

                  {this.renderError('password')}
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
                    id="confirm-password-input"
                    name="confirm_password"
                    type="password"
                    placeholder="Confirm password"
                    value={confirmPasswordInput}
                    className={signupErrors.confirmPassword ? 'error' : ''}
                    onChange={this.onConfirmPasswordInputChange}
                  />

                  {this.renderError('confirmPassword')}
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
                    label="Signup"
                    type="submit"
                    className="signup-button"
                    disabled={signingUp}
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

export default Signup
