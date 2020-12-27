import React, { Component } from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import { Button, Table, Container, Grid, Image } from "semantic-ui-react";
import Gallery from "react-grid-gallery";

class GridGallery extends Component {
  state = { images: [] };

  constructor(props) {
    super(props);

    this.updateImages(this.props.images);
  }

  componentDidUpdate(prevProps) {
    if (prevProps.images !== this.props.images) {
      this.updateImages(this.props.images);
    }
  }

  updateImages(images) {
    if (!images) {
      images = [];
    }
    // console.log(images);
    this.setState({ images });
  }

  render() {
    const { images } = this.state;
    const columns = 8;
    const numberOfRow = parseInt((images.length - 1) / columns + 1);

    return (
      <Grid>
        {[...Array(numberOfRow).keys()].map((row) => {
          if ((row + 1) * columns > images.length) {
            return (
              <Grid.Row columns={columns}>
                {[...Array(images.length % columns).keys()].map((column) => {
                  return (
                    <Grid.Column>
                      <Image
                        src={images[column + row * columns].src}
                        style={{
                          width: "100%",
                          height: "100%",
                          "object-fit": "cover",
                        }}
                        bordered
                      />
                    </Grid.Column>
                  );
                })}
              </Grid.Row>
            );
          } else {
            return (
              <Grid.Row columns={columns}>
                {[...Array(columns).keys()].map((column) => {
                  return (
                    <Grid.Column>
                      <Image
                        src={images[column + row * columns].src}
                        style={{
                          width: "100%",
                          height: "100%",
                          "object-fit": "cover",
                        }}
                        bordered
                      />
                    </Grid.Column>
                  );
                })}
              </Grid.Row>
            );
          }
        })}
      </Grid>
    );
  }
}

export default GridGallery;
