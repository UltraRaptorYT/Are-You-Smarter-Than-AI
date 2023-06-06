FROM tensorflow/serving

WORKDIR /

COPY models/model_config.config /models/model_config.config
COPY models/Cifar20CustomVGG16 /models/Cifar20CustomVGG16
COPY models/Cifar20Efficient /models/Cifar20Efficient
COPY models/Cifar100CustomVGG16 /models/Cifar100CustomVGG16
COPY models/Cifar100Efficient /models/Cifar100Efficient

CMD ["--model_config_file=/models/model_config.config"]
