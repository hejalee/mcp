import { defineFunction } from "@aws-amplify/backend";

export const myFunction = defineFunction({
  name: "my-function",
  layers: {
   "@aws-lambda-powertools/logger":
      "arn:aws:lambda:us-east-1:094274105915:layer:AWSLambdaPowertoolsTypeScriptV2:12",
  },
});